1. What is the difference between NLP, NLU, and NLG?
NLP is the overall field that helps computers work with human language. NLU focuses on understanding the meaning, while NLG focuses on generating human-like text.

2. Why can the word “bank” require different representations in different sentences?
The word “bank” can have different meanings depending on the context. For example, “river bank” and “bank account” refer to completely different things, so NLP models need to represent them differently.

3. What does tokenization do?
Tokenization breaks text into smaller pieces called tokens, such as words, subwords, or characters. These tokens can then be processed by an NLP model.

4. Why might removing stop words damage sentiment analysis?
Some stop words can completely change the sentiment of a sentence. For example, removing “not” from “The movie is not good” would change its meaning.

5. What information does Bag of Words discard?
Bag of Words mainly keeps track of which words appear and how often. It ignores word order, grammar, and much of the context of the sentence.

6. Why does TF-IDF reduce the weight of terms found in many documents?
Words that appear in almost every document usually don’t tell us much about what makes a document unique. TF-IDF therefore gives more importance to distinctive words and less to very common ones.

7. How do static and contextual embeddings differ?
Static embeddings give a word the same representation every time, regardless of where it is used. Contextual embeddings change the representation based on the surrounding words and meaning.

8. What role does positional information play in a Transformer?
Transformers process words together rather than naturally following their order. Positional information helps the model understand where each token appears in the sentence and therefore understand word order.

9. Which Transformer variant is commonly used for embeddings and classification?
Encoder-based Transformers, such as BERT, are commonly used for embeddings and classification tasks. They are good at understanding the context and meaning of input text.

10. Why should NLP evaluation use more than one average metric?
A single average metric may hide areas where the model performs poorly. Using multiple metrics, such as precision, recall, and F1-score, gives a more complete picture of the model’s performance.
