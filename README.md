# wolfdotsolar
Helpers to improve Solar Observation Processing Pipeline

## Build
```
./Docker/buildDockerImage.sh
```

## Crop Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/:/imgs isontheline/wolfdotsolar:latest crop_sun /imgs/*.JPG
```

## Stack Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/wolfdotsolar/crop/:/imgs/ isontheline/wolfdotsolar:latest PlanetarySystemStacker /imgs/ --stack_percent=50
```

## Unsharp Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/wolfdotsolar/crop/:/imgs isontheline/wolfdotsolar:latest unsharp /imgs/_pss.png --amount=3 --sigma=3 --radius=100
```

## Example Result
![Sun Cropped and Stacked with wolfdotsolar](/samples/sun-cropped-and-stacked-with-wolfdotsolar.jpg)