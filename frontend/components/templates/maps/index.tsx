"use client";

import { FC } from "react";
import { Polygon, Placemark, YMaps, Map } from '@pbe/react-yandex-maps';
import { useMaps } from "./index.hooks";

interface MapsTemplateProps { }

const MapsTemplate: FC<MapsTemplateProps> = () => {
    const { mapCenter, placeMarks } = useMaps();

    return (
        <YMaps>
            <Map
                defaultState={{
                    center: mapCenter,
                    zoom: 10,
                }}
                className="w-full h-full"
            >
                {placeMarks.map((placeMark, index) => (
                    <Placemark
                        key={index}
                        geometry={placeMark.geometry}
                        properties={placeMark.properties}
                        modules={["geoObject.addon.hint"]}
                        options={{
                            iconColor: "#ff0000",
                        }}
                    />
                ))}
            </Map>
        </YMaps>
    )
};

export default MapsTemplate;
