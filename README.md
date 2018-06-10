# Monte Carlo #

![track_1](images/track_1.svg)
![track_2](images/track_2.svg)
![track_3](images/track_3.svg)

```
for track in track_1 track_2 track_3;
  do python -m scripts.show_racetrack "$track" --save-path "images/$track.svg";
done
```