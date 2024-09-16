from wordllama import WordLlama
from .vectordb import VectorDB

# wl = WordLlama.load(config = "D:/projects/embedder/embedder.toml")
wl = WordLlama.load()
similarity_score = wl.similarity("i went to the car", "i went to the pawn shop")
print(similarity_score)  # Output: 0.06641249096796882

db = VectorDB(collection_name="test-vector-db", 
              database="embedder.sqlite")


# Rank documents based on their similarity to a query
query = "i went to the car"
candidates = ["i went to the park", "i went to the shop", "i went to the truck", "i went to the vehicle"]

print("Ranking documents...")
print(wl.embed(query))
print(wl.embed(candidates))


ranked_docs = wl.rank(query, candidates)



print(ranked_docs)


