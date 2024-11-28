from shortlister.tournament import get_pair

mylist = [1,2,3,4,5,6,7]

def test_get_pair():
    result = get_pair(mylist)
    expected = [(1, 2),(1, 3),(1, 4),(1, 5),(1, 6),(1, 7),(2, 3),(2, 4),(2, 5),(2, 6),(2, 7),(3, 4),(3, 5),(3, 6),(3, 7),(4, 5),(4, 6),(4, 7),(5, 6),(5, 7),(6, 7)]
    for item in result:
        assert result.count(item) == 1
    assert result == expected