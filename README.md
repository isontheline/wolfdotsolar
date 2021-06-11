# wolfdotsolar
Solar Observation Processing Pipeline

## 1. Build Docker Image (optional)
```
./Docker/buildDockerImage.sh
```

## 2. Launch Crop & Stack Pipeline
```
docker run --rm -v /folder/with/sun/pictures/:/imgs isontheline/wolfdotsolar:edge cropnstack "/imgs/*.JPG"
```

## 3. Examples of Results
<img src="./samples/sun-cropped-and-stacked-with-wolfdotsolar.jpg" alt="Sun Cropped and Stacked with wolfdotsolar" style="width:45%"/>

<img src="./samples/solar-eclipse-20210610-0950-arnac-pompadour-france.jpg" alt="Solar Eclipse June 10, 2021 at Arnac-Pompadour" style="width:45%"/>
