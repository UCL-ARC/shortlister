from shortlister.tournament import get_pair, rank

mylist = [
    "apple", "banana", "bike", "bottle", "book", "car", "cat", "chair", 
    "door", "dog", "laptop", "moon", "mountain", "pen", "phone", "river", 
    "sun", "table", "tree", "window"
]

sample_result = {
    ("apple", "banana"): "apple",
    ("car", "bike"): "car",
    ("cat", "dog"): "dog",
    ("sun", "moon"): "moon",
    ("table", "chair"): "chair",
    ("tree", "river"): "tree",
    ("mountain", "book"): "book",
    ("pen", "phone"): "pen",
    ("laptop", "bottle"): "bottle",
    ("window", "door"): "door",
    ("apple", "car"): "apple",
    ("banana", "dog"): "dog",
    ("bike", "tree"): "bike",
    ("cat", "moon"): "moon",
    ("sun", "mountain"): "sun",
    ("chair", "river"): "river",
    ("table", "laptop"): "laptop",
    ("bottle", "window"): "bottle",
    ("book", "door"): "book",
    ("pen", "phone"): "phone",
}


def test_get_pair():
    result = get_pair(mylist)
    expected = [(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(1, 7),(2, 3),(2, 4),(2, 5),(2, 6),(2, 7),(3, 4),(3, 5),(3, 6),(3, 7),(4, 5),(4, 6),(4, 7),(5, 6),(5, 7),(6, 7)]
    for item in result:
        assert result.count(item) == 1
    assert result == expected



def test_rank():
    rank(mylist)