"use client";

import React, { FC } from "react";
import { useMaps } from "./index.hooks";
import PlanDialogEdit from "@/components/molecules/plan-dialog-edit";
import { Button } from "@/components/ui/button";
import {
  Circle,
  CircleXIcon,
  MapPin,
  MapPinOff,
  PackageOpenIcon,
  PenBoxIcon,
} from "lucide-react";
import {
  calendarRangeDuration,
  cn,
  formatPrice,
  managerFullName,
} from "@/lib/utils";
import { TengeReciept } from "@/components/icons/tenge-reciept";
import { Slider } from "@/components/ui/slider";
import { Label } from "@radix-ui/react-label";
import PlanDialogNew from "@/components/molecules/plan-dialog-new";
import useFiltersContext from "@/components/molecules/side-bar/index.providers";
import MaxDaysAlert from "./max-days-alert";

interface MapsTemplateProps {}

const MapsTemplate: FC<MapsTemplateProps> = () => {
  const {
    mapElementRef,
    selectedPlan,
    setSelectedPlanId,
    isPlansLoading,
    isShowingClientsNearby,
    handleShowingClientsNearby,
    clientSearchRadius,
    setClientSearchRadius,
    minDaysSincePlan,
    setMinDaysSincePlan,
    selectedNearbyClient,
    setSelectedNearbyClient,
  } = useMaps();

  const { calendarRange } = useFiltersContext();
  if (calendarRange && calendarRangeDuration(calendarRange) >= 31) {
    return <MaxDaysAlert />;
  }

  return (
    <div className="flex h-full gap-4">
      {isPlansLoading && (
        <Circle className="absolute top-[calc(50%-1rem)] left-[calc(50%-1rem)] z-10 w-8 h-8 animate-ping text-gray-300" />
      )}
      <div
        className="flex-1 h-full rounded-lg overflow-clip duration-300"
        style={{ minHeight: "500px" }}
        ref={mapElementRef}
      />
      <div
        className={cn(
          "h-full overflow-y-auto duration-300",
          selectedPlan ? "w-96" : "w-0",
        )}
      >
        {selectedPlan && (
          <div
            className="flex flex-col gap-4 relative pt-8"
            key={selectedPlan.id}
          >
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
                <span>{formatPrice(selectedPlan.shipment_cost)}</span>
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

              <Button className="flex-1" onClick={handleShowingClientsNearby}>
                {isShowingClientsNearby ? (
                  <>
                    <MapPinOff className="w-5 h-5 mr-2" />
                    Скрыть клиентов
                  </>
                ) : (
                  <>
                    <MapPin className="w-5 h-5 mr-2" />
                    Клиенты рядом
                  </>
                )}
              </Button>
            </div>
            {isShowingClientsNearby && (
              <div>
                <div className="grid grid-cols-2 items-center gap-2 mb-4">
                  <Label
                    htmlFor="radius"
                    className="text-sm font-semibold text-nowrap"
                  >
                    Радиус поиска: {clientSearchRadius} км
                  </Label>
                  <Slider
                    id="radius"
                    min={1}
                    max={10}
                    step={1}
                    value={[clientSearchRadius]}
                    onValueChange={(value) => setClientSearchRadius(value[0])}
                  />
                  <Label
                    htmlFor="minDaysSincePlan"
                    className="text-sm font-semibold text-nowrap"
                  >
                    С посещения: &gt; {minDaysSincePlan} дней
                  </Label>
                  <Slider
                    id="minDaysSincePlan"
                    min={1}
                    max={30}
                    step={1}
                    value={[minDaysSincePlan]}
                    onValueChange={(value) => setMinDaysSincePlan(value[0])}
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
      {selectedNearbyClient && selectedPlan && (
        <PlanDialogNew
          defaultIsOpen={true}
          defaultHandleOpen={() => setSelectedNearbyClient(undefined)}
          defaultClientId={selectedNearbyClient}
          defaultAssignedDate={selectedPlan.assigned_date || undefined}
        />
      )}
    </div>
  );
};

export default MapsTemplate;
