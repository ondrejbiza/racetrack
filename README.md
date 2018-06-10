# Monte Carlo #

![track_1](images/track_1.svg)
![track_2](images/track_2.svg)
![track_3](images/track_3.svg)

```
for track in track_1 track_2 track_3;
  do python -m scripts.show_racetrack "$track" --save-path "images/$track.svg";
done
```

![track_1_episode_1](images/track_1_episode_1.svg)
![track_1_episode_2](images/track_1_episode_2.svg)
![track_1_episode_3](images/track_1_episode_3.svg)

```
python -m scripts.solve_racetrack track_1 0.1 --save-path images/track_1_episode
```

![track_2_episode_1](images/track_2_episode_1.svg)
![track_2_episode_3](images/track_2_episode_3.svg)
![track_2_episode_5](images/track_2_episode_5.svg)

```
python -m scripts.solve_racetrack track_2 0.1 --save-path images/track_2_episode
```

![track_3_episode_1](images/track_3_episode_1.svg)
![track_3_episode_9](images/track_3_episode_9.svg)
![track_3_episode_19](images/track_3_episode_19.svg)

```
python -m scripts.solve_racetrack track_3 0.1 --save-path images/track_3_episode
```