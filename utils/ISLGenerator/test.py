# Custom Lib Import
import ISL_converter 

def main():
    # Initialize
    converter = ISL_converter.ISLConverter()

    # Test sentences
    sentences = [
        "The cat is sleeping on the mat.",
        "I am going to the market.",
        "She likes to read books in the library.",
        "The quick brown fox jumps over the lazy dog.",
        "Hello, world! How are you?",
        "The cats are running in the fields."
    ]

    # Convert each sentence and print the result
    for sentence in sentences:
        isl_sentence = converter.text_to_isl(sentence)
        print(f"English: {sentence}")
        print(f"ISL: {isl_sentence}")
        print()

if __name__ == "__main__":
    main()