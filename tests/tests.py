def test_sequence_1(client):
    assert client.get("/set?name=ex&value=10").text == "ex = 10"
    assert client.get("/get?name=ex").text == "10"
    assert client.get("/unset?name=ex").text == "ex = None"
    assert client.get("/get?name=ex").text == "None"
    assert client.get("/end").text == "CLEANED"


def test_sequence_2(client):
    assert client.get("/set?name=a&value=10").text == "a = 10"
    assert client.get("/set?name=b&value=10").text == "b = 10"
    assert client.get("/numequalto?value=10").text == "2"
    assert client.get("/numequalto?value=20").text == "0"
    assert client.get("/set?name=b&value=30").text == "b = 30"
    assert client.get("/numequalto?value=10").text == "1"
    assert client.get("/end").text == "CLEANED"


def test_sequence_3(client):
    assert client.get("/set?name=a&value=10").text == "a = 10"
    assert client.get("/set?name=b&value=20").text == "b = 20"
    assert client.get("/get?name=a").text == "10"
    assert client.get("/get?name=b").text == "20"
    assert client.get("/undo").text == "b = None"
    assert client.get("/get?name=a").text == "10"
    assert client.get("/get?name=b").text == "None"
    assert client.get("/set?name=a&value=40").text == "a = 40"
    assert client.get("/get?name=a").text == "40"
    assert client.get("/undo").text == "a = 10"
    assert client.get("/get?name=a").text == "10"
    assert client.get("/undo").text == "a = None"
    assert client.get("/get?name=a").text == "None"
    assert client.get("/undo").text == "NO COMMANDS"
    assert client.get("/redo").text == "a = 10"
    assert client.get("/redo").text == "a = 40"
    assert client.get("/end").text == "CLEANED"


def test_undo_redo(client):
    initial_b = client.get("/get?name=b").text
    client.get("/set?name=a&value=10")
    client.get("/set?name=b&value=20")
    client.get("/unset?name=a")
    assert client.get("/undo").text == "a = 10"
    assert client.get("/undo").text == f"b = {initial_b}"
    assert client.get("/redo").text == "b = 20"
    assert client.get("/redo").text == "a = None"
    client.get("/set?name=a&value=30")
    assert client.get("/redo").text == "NO COMMANDS"
    assert client.get("/end").text == "CLEANED"
