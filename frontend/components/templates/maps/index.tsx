"use client";

import { FC } from "react";
import { Polygon, YMaps, Map } from '@pbe/react-yandex-maps';

interface MapsTemplateProps { }

const MapsTemplate: FC<MapsTemplateProps> = () => {
    return (
        <YMaps>
            <Map
                defaultState={{
                    center: [55.73, 37.9],
                    zoom: 10,
                }}
                className="w-full h-full rounded-lg overflow-clip"
            >
                <Polygon
                    geometry={[
                        [
                            [55.75, 37.8],
                            [55.8, 37.9],
                            [55.75, 38.0],
                            [55.7, 38.0],
                            [55.7, 37.8],
                        ],
                        [
                            [55.75, 37.82],
                            [55.75, 37.98],
                            [55.65, 37.9],
                        ],
                    ]}
                    options={{
                        fillColor: "#00FF00",
                        strokeColor: "#0000FF",
                        opacity: 0.5,
                        strokeWidth: 5,
                        strokeStyle: "shortdash",
                    }}
                />
            </Map>
        </YMaps>
    )
};

export default MapsTemplate;
