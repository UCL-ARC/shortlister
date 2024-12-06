from shortlister.tournament import get_pair, rank

mylist = [
    "apple",
    "banana",
    "bike",
    "bottle",
    "book",
    "car",
    "cat",
    "chair",
    "door",
    "dog",
    "laptop",
    "moon",
    "mountain",
    "pen",
    "phone",
    "river",
    "sun",
    "table",
    "tree",
    "window",
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
    for item in result:
        assert result.count(item) == 1


def test_rank():
    result = rank(mylist, sample_result)
    assert result == [
        "apple",
        "bottle",
        "book",
        "dog",
        "moon",
        "bike",
        "car",
        "chair",
        "door",
        "laptop",
        "phone",
        "river",
        "sun",
        "tree",
        "banana",
        "cat",
        "mountain",
        "pen",
        "table",
        "window",
    ]
