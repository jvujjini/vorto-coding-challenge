To run the program:

```
python3/python vrp.py [input_data_path]
```

Notes:

This is a fairly straight forward code trying to prioritize for the drive times of the drivers. And a basic version of cost optimization by picking the next load to be the neareast point to the curr location.

To-Do:

- If I had further time, I would try to optimize this by using a clustering algorithm(for example: nearest neighbor) to cluster the points. 
- There after we can send one driver over to each cluster until we hit the drive time limit.
- Send the next driver to the next point in the previous cluster if it is not done and so on.
- If the current driver has time limit, we can attempt to send them to the next cluster and see if the next load can be achieved. If yes, continue in that cluster until time limit is hit and so on.