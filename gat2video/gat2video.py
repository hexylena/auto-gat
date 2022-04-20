
def runningGroup(steps):
    c = None
    for step in steps:
        if c is None:
            c = [step]
            continue

        # If the new visual is different, then
        if step["data"]["visual"] != c[-1]["data"]["visual"]:
            # Yield the current list
            yield c
            # And reset it with current step
            c = [step]
        else:
            c.append(step)
    yield c
