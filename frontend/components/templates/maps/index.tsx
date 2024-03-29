"use client";

import { FC } from "react";
import { Polygon, Placemark, YMaps, Map } from '@pbe/react-yandex-maps';
import { useMaps } from "./index.hooks";

interface MapsTemplateProps { }

const MapsTemplate: FC<MapsTemplateProps> = () => {
    const { mapCenter, placeMarks, polygons } = useMaps();

    return (
        <YMaps>
            <Map
                defaultState={{
                    center: mapCenter,
                    zoom: 12,
                }}
                className="w-full h-full"
            >
                {placeMarks.map((placeMark, index) => (
                    <Placemark
                        key={index}
                        geometry={placeMark.geometry}
                        properties={placeMark.properties}
                        options={placeMark.options}
                        modules={["geoObject.addon.balloon", "geoObject.addon.hint"]}
                    />
                ))}
                {polygons.map((polygon, index) => (
                    <Polygon
                        key={index}
                        geometry={polygon.geometry}
                        options={polygon.options}
                        modules={["geoObject.addon.balloon", "geoObject.addon.hint"]}
                    />
                ))}
            </Map>
        </YMaps>
    )
};

export default MapsTemplate;
