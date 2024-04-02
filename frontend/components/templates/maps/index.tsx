"use client";

import { FC } from "react";
import { Polygon, Placemark, YMaps, Map } from "@pbe/react-yandex-maps";
import { useMaps } from "./index.hooks";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";
import { Button } from "@/components/ui/button";
import {
  CircleXIcon,
  Earth,
  PackageOpenIcon,
  Pen,
  PenBoxIcon,
  PenIcon,
  XIcon,
} from "lucide-react";
import { cn, managerFullName } from "@/lib/utils";
import { TengeReciept } from "@/components/icons/tenge-reciept";

interface MapsTemplateProps {}

const MapsTemplate: FC<MapsTemplateProps> = () => {
  const { mapCenter, placeMarks, polygons, selectedPlan, setSelectedPlanId } =
    useMaps();

  return (
    <div className="flex h-full gap-4">
      <YMaps>
        <Map
          defaultState={{
            center: mapCenter,
            zoom: 12,
          }}
          className="flex-1 h-full rounded-lg overflow-clip duration-300"
        >
          {placeMarks.map((placeMark, index) => (
            <Placemark
              key={index}
              {...placeMark}
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
      <div
        className={cn(
          "h-full overflow-y-auto duration-300",
          selectedPlan ? "w-96" : "w-0",
        )}
      >
        {selectedPlan && (
          <div className="flex flex-col gap-4 relative pt-8">
            <div className="text-lg font-bold">
              План отгрузки{" "}
              {new Date(selectedPlan.assigned_date).toLocaleString("ru-RU", {
                day: "numeric",
                month: "long",
                year: "numeric",
              })}
            </div>
            <CircleXIcon
              className="fill-red-400 stroke-red-700 w-6 h-6 cursor-pointer absolute top-2 right-0"
              onClick={() => setSelectedPlanId(undefined)}
            />
            <div className="w-full">
              <div
                className="text-lg font-bold line-clamp-1 text-ellipsis"
                title={selectedPlan.client.name}
              >
                {selectedPlan.client.name}
              </div>
              <div className="text-sm text-muted-foreground line-clamp-1 text-ellipsis">
                {selectedPlan.client.address.street}
              </div>
            </div>

            <div>
              <div className="font-semibold">Менеджеры:</div>
              <div className="grid grid-cols-3">
                {selectedPlan.managers
                  .sort((a, b) => a.first_name.localeCompare(b.first_name))
                  .map((manager) => (
                    <div key={manager.id}>{managerFullName(manager)}</div>
                  ))}
              </div>
            </div>

            <div>
              <div className="font-semibold">Работы:</div>
              <div className="grid grid-cols-3">
                {selectedPlan.worklist
                  .sort((a, b) => a.name.localeCompare(b.name))
                  .map((work) => (
                    <div key={work.id}>{work.name}</div>
                  ))}
              </div>
            </div>

            <div>
              <div className="font-semibold">Детали:</div>
              <div className="grid grid-cols-2 items-center">
                <span className="flex items-center">
                  <TengeReciept className="w-5 h-5 mr-2" />
                  Сумма отгрузки
                </span>
                <span>{selectedPlan.shipment_cost}</span>
              </div>
              <div className="grid grid-cols-2">
                <span className="flex items-center">
                  <PackageOpenIcon className="w-5 h-5 mr-2" />
                  Кол. коробок
                </span>
                <span>{selectedPlan.box_count}</span>
              </div>
            </div>

            <div className="w-full gap-2 flex flex-row">
              <PlanDialogEdit plan={selectedPlan}>
                <Button className="flex-1">
                  <PenBoxIcon className="w-5 h-5 mr-2" />
                  Изменить
                </Button>
              </PlanDialogEdit>

              <Button className="flex-1">
                <Earth className="w-5 h-5 mr-2" />
                Клиенты рядом
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapsTemplate;
