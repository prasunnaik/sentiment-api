/**
 * Service responsible for calculating staff dashboard metrics.
 *
 * <p>Metrics are aggregated from customer, staff, category, policy,
 * application, claim, and payment data.</p>
 */
@Service
@Transactional(readOnly = true)
public class DashboardService {





/**
 * Retrieves aggregate metrics used by the staff dashboard.
 *
 * @return dashboard metrics containing customer, staff, category,
 *         policy, application, claim, and payment counts
 */
public DashboardMetricsResponse getMetrics() {






/**
 * Counts all rows in the specified database table.
 *
 * @param tableName database table name
 * @return number of rows in the table
 */
private long countTable(String tableName) {






/**
 * Counts rows in a database table having the specified status.
 *
 * @param tableName database table name
 * @param status status value to match
 * @return number of matching rows
 */
private long countByStatus(String tableName, String status) {






