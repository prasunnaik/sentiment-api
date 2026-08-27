package com.its.issue.lambda;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyRequestEvent;
import com.amazonaws.services.lambda.runtime.events.APIGatewayProxyResponseEvent;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.sql.*;
import java.time.LocalDateTime;
import java.util.*;

public class IssueLambdaHandler
        implements RequestHandler<APIGatewayProxyRequestEvent, APIGatewayProxyResponseEvent> {

    private final ObjectMapper mapper = new ObjectMapper();

    private final String DB_URL =
            "jdbc:mysql://its.cinei2gc4el7.us-east-1.rds.amazonaws.com:3306/issue_db";

    private final String DB_USER = "root";
    private final String DB_PASSWORD = "password";

    @Override
    public APIGatewayProxyResponseEvent handleRequest(
            APIGatewayProxyRequestEvent event,
            Context context) {

        try {
            String method = event.getHttpMethod();
            String path = event.getPath();

            if ("POST".equals(method) && path.equals("/api/issues")) {
                return createIssue(event);
            }

            if ("GET".equals(method) && path.equals("/api/issues")) {
                return getAllIssues();
            }

            if ("GET".equals(method) && path.matches("/api/issues/\\d+")) {
                Long id = Long.parseLong(path.substring(path.lastIndexOf("/") + 1));
                return getIssueById(id);
            }

            if ("PUT".equals(method) && path.matches("/api/issues/\\d+/status")) {
                Long id = Long.parseLong(path.split("/")[3]);
                return updateStatus(id, event);
            }

            if ("PUT".equals(method) && path.matches("/api/issues/\\d+/priority")) {
                Long id = Long.parseLong(path.split("/")[3]);
                return updatePriority(id, event);
            }

            if ("PUT".equals(method) && path.matches("/api/issues/\\d+/assignee/\\d+")) {
                String[] parts = path.split("/");
                Long issueId = Long.parseLong(parts[3]);
                Long assigneeId = Long.parseLong(parts[5]);

                return updateAssignee(issueId, assigneeId);
            }

            if ("PUT".equals(method) && path.matches("/api/issues/\\d+")) {
                Long id = Long.parseLong(path.substring(path.lastIndexOf("/") + 1));
                return updateIssue(id, event);
            }

            if ("DELETE".equals(method) && path.matches("/api/issues/\\d+")) {
                Long id = Long.parseLong(path.substring(path.lastIndexOf("/") + 1));
                return deleteIssue(id);
            }

            if ("GET".equals(method) && path.matches("/api/issues/project/\\d+")) {
                Long projectId = Long.parseLong(path.substring(path.lastIndexOf("/") + 1));
                return getIssuesByProject(projectId);
            }

            if ("GET".equals(method) && path.matches("/api/issues/assignee/\\d+")) {
                Long assigneeId = Long.parseLong(path.substring(path.lastIndexOf("/") + 1));
                return getIssuesByAssignee(assigneeId);
            }

            return response(404, Map.of("message", "Endpoint not found"));

        } catch (Exception e) {
            e.printStackTrace();
            return response(500, Map.of("message", e.getMessage()));
        }
    }

    private Connection connection() throws SQLException {
        return DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
    }

    private APIGatewayProxyResponseEvent createIssue(
            APIGatewayProxyRequestEvent event) throws Exception {

        Map<String, Object> data =
                mapper.readValue(event.getBody(), Map.class);

        String sql = """
                INSERT INTO issues
                (summary, description, priority, assignee_id, status,
                 created_date, last_updated_date, project_id,
                 sprint, story_point, tags, type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;

        LocalDateTime now = LocalDateTime.now();

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(
                     sql, Statement.RETURN_GENERATED_KEYS)) {

            ps.setString(1, (String) data.get("summary"));
            ps.setString(2, (String) data.get("description"));
            ps.setString(3, (String) data.get("priority"));
            ps.setLong(4, ((Number) data.get("assigneeId")).longValue());
            ps.setString(5, (String) data.get("status"));
            ps.setTimestamp(6, Timestamp.valueOf(now));
            ps.setTimestamp(7, Timestamp.valueOf(now));
            ps.setLong(8, ((Number) data.get("projectId")).longValue());
            ps.setString(9, (String) data.get("sprint"));

            if (data.get("storyPoint") == null)
                ps.setNull(10, Types.INTEGER);
            else
                ps.setInt(10, ((Number) data.get("storyPoint")).intValue());

            ps.setString(11, (String) data.get("tags"));
            ps.setString(12, (String) data.get("type"));

            ps.executeUpdate();

            ResultSet rs = ps.getGeneratedKeys();

            if (rs.next()) {
                Map<String, Object> result = new HashMap<>(data);
                result.put("id", rs.getLong(1));
                result.put("createdDate", now.toString());
                result.put("lastUpdatedDate", now.toString());

                return response(201, result);
            }
        }

        return response(500, Map.of("message", "Issue creation failed"));
    }

    private APIGatewayProxyResponseEvent getAllIssues()
            throws Exception {

        String sql = "SELECT * FROM issues";

        List<Map<String, Object>> issues = new ArrayList<>();

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                issues.add(toMap(rs));
            }
        }

        return response(200, issues);
    }

    private APIGatewayProxyResponseEvent getIssueById(Long id)
            throws Exception {

        String sql = "SELECT * FROM issues WHERE id = ?";

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setLong(1, id);

            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                return response(200, toMap(rs));
            }
        }

        return response(404,
                Map.of("message", "Issue not found with id: " + id));
    }

    private APIGatewayProxyResponseEvent updateIssue(
            Long id,
            APIGatewayProxyRequestEvent event) throws Exception {

        Map<String, Object> data =
                mapper.readValue(event.getBody(), Map.class);

        String sql = """
                UPDATE issues SET
                summary=?,
                description=?,
                priority=?,
                assignee_id=?,
                status=?,
                project_id=?,
                sprint=?,
                story_point=?,
                tags=?,
                type=?,
                last_updated_date=?
                WHERE id=?
                """;

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setString(1, (String) data.get("summary"));
            ps.setString(2, (String) data.get("description"));
            ps.setString(3, (String) data.get("priority"));
            ps.setLong(4, ((Number) data.get("assigneeId")).longValue());
            ps.setString(5, (String) data.get("status"));
            ps.setLong(6, ((Number) data.get("projectId")).longValue());
            ps.setString(7, (String) data.get("sprint"));

            if (data.get("storyPoint") == null)
                ps.setNull(8, Types.INTEGER);
            else
                ps.setInt(8, ((Number) data.get("storyPoint")).intValue());

            ps.setString(9, (String) data.get("tags"));
            ps.setString(10, (String) data.get("type"));
            ps.setTimestamp(11,
                    Timestamp.valueOf(LocalDateTime.now()));
            ps.setLong(12, id);

            int rows = ps.executeUpdate();

            if (rows == 0) {
                return response(404,
                        Map.of("message", "Issue not found"));
            }
        }

        return getIssueById(id);
    }

    private APIGatewayProxyResponseEvent updateStatus(
            Long id,
            APIGatewayProxyRequestEvent event) throws Exception {

        Map<String, Object> data =
                mapper.readValue(event.getBody(), Map.class);

        return simpleUpdate(
                "status",
                data.get("status"),
                id);
    }

    private APIGatewayProxyResponseEvent updatePriority(
            Long id,
            APIGatewayProxyRequestEvent event) throws Exception {

        Map<String, Object> data =
                mapper.readValue(event.getBody(), Map.class);

        return simpleUpdate(
                "priority",
                data.get("priority"),
                id);
    }

    private APIGatewayProxyResponseEvent updateAssignee(
            Long issueId,
            Long assigneeId) throws Exception {

        return simpleUpdate(
                "assignee_id",
                assigneeId,
                issueId);
    }

    private APIGatewayProxyResponseEvent simpleUpdate(
            String column,
            Object value,
            Long id) throws Exception {

        String sql =
                "UPDATE issues SET " + column +
                "=?, last_updated_date=? WHERE id=?";

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            if (value instanceof Number)
                ps.setLong(1, ((Number) value).longValue());
            else
                ps.setString(1, String.valueOf(value));

            ps.setTimestamp(2,
                    Timestamp.valueOf(LocalDateTime.now()));

            ps.setLong(3, id);

            int rows = ps.executeUpdate();

            if (rows == 0) {
                return response(404,
                        Map.of("message", "Issue not found"));
            }
        }

        return getIssueById(id);
    }

    private APIGatewayProxyResponseEvent deleteIssue(Long id)
            throws Exception {

        String sql = "DELETE FROM issues WHERE id=?";

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setLong(1, id);

            int rows = ps.executeUpdate();

            if (rows == 0) {
                return response(404,
                        Map.of("message", "Issue not found"));
            }
        }

        return new APIGatewayProxyResponseEvent()
                .withStatusCode(204);
    }

    private APIGatewayProxyResponseEvent getIssuesByProject(
            Long projectId) throws Exception {

        return getByColumn("project_id", projectId);
    }

    private APIGatewayProxyResponseEvent getIssuesByAssignee(
            Long assigneeId) throws Exception {

        return getByColumn("assignee_id", assigneeId);
    }

    private APIGatewayProxyResponseEvent getByColumn(
            String column,
            Long value) throws Exception {

        String sql =
                "SELECT * FROM issues WHERE " + column + "=?";

        List<Map<String, Object>> issues = new ArrayList<>();

        try (Connection con = connection();
             PreparedStatement ps = con.prepareStatement(sql)) {

            ps.setLong(1, value);

            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
                issues.add(toMap(rs));
            }
        }

        return response(200, issues);
    }

    private Map<String, Object> toMap(ResultSet rs)
            throws SQLException {

        Map<String, Object> map = new LinkedHashMap<>();

        map.put("id", rs.getLong("id"));
        map.put("summary", rs.getString("summary"));
        map.put("description", rs.getString("description"));
        map.put("priority", rs.getString("priority"));
        map.put("assigneeId", rs.getLong("assignee_id"));
        map.put("status", rs.getString("status"));
        map.put("createdDate",
                rs.getTimestamp("created_date"));
        map.put("lastUpdatedDate",
                rs.getTimestamp("last_updated_date"));
        map.put("projectId", rs.getLong("project_id"));
        map.put("sprint", rs.getString("sprint"));
        map.put("storyPoint", rs.getObject("story_point"));
        map.put("tags", rs.getString("tags"));
        map.put("type", rs.getString("type"));

        return map;
    }

    private APIGatewayProxyResponseEvent response(
            int status,
            Object body) {

        try {
            return new APIGatewayProxyResponseEvent()
                    .withStatusCode(status)
                    .withHeaders(Map.of(
                            "Content-Type", "application/json",
                            "Access-Control-Allow-Origin", "*",
                            "Access-Control-Allow-Headers", "*",
                            "Access-Control-Allow-Methods",
                            "GET,POST,PUT,DELETE,OPTIONS"))
                    .withBody(mapper.writeValueAsString(body));

        } catch (Exception e) {
            return new APIGatewayProxyResponseEvent()
                    .withStatusCode(500)
                    .withBody("{\"message\":\"Response creation failed\"}");
        }
    }
}
