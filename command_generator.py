tests: dict[str, str] = {
    "test_astar_h1": "solve a-star h1",
    "test_astar_h2": "solve a-star h2",
    "test_beam_k15": "solve beam 15",
    "test_beam_k75": "solve beam 75",
    "test_beam_k150": "solve beam 150"
}

for test, command in tests.items():
    with open(test, "w") as file:
        file.write("time\n")
        for i in range(1, 501):
            file.write("setState 012345678\n")
            file.write(f"randomizeState {i}" + "\n")
            file.write(command + "\n")