"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Star, LayoutGrid, LayoutList } from "lucide-react";
import { FC, useState, useMemo, useCallback } from "react";
import { cn, managerFullName, managerShortName } from "@/lib/utils";

const MAX_BEST_ROUTE_KM_DELTA = 100;

export type ManagerDisplayMode = "compact" | "detailed";

interface ManagerGroup {
  label: string;
  managers: Manager[];
  bestId: string | null;
}

export interface SelectManagersProps {
  id?: string;
  allManagers: Manager[];
  switchManager: (id: string) => void;
  selectedManagers: string[];
  scores?: ManagerScore[];
  scoresLoading?: boolean;
  displayMode?: ManagerDisplayMode;
  onDisplayModeChange?: (mode: ManagerDisplayMode) => void;
}

const SectionLabel: FC<{ children: string }> = ({ children }) => (
  <span className="text-[11px] text-muted-foreground uppercase tracking-wide">
    {children}
  </span>
);

interface ManagerRowDetailedProps {
  manager: Manager;
  selectedManagers: string[];
  switchManager: (id: string) => void;
  score: ManagerScore | undefined;
  isBest: boolean;
  scoresLoading?: boolean;
}

const ManagerRowDetailed: FC<ManagerRowDetailedProps> = ({
  manager,
  selectedManagers,
  switchManager,
  score,
  isBest,
  scoresLoading,
}) => {
  const isDayOff = score?.is_day_off;

  return (
    <div className="flex items-center gap-2">
      <Checkbox
        id={`manager-${manager.id}`}
        onClick={() => !isDayOff && switchManager(manager.id)}
        checked={selectedManagers.includes(manager.id)}
        disabled={isDayOff}
      />
      <Label
        className={cn(
          "font-normal flex-1",
          isDayOff ? "text-muted-foreground" : "hover:cursor-pointer",
        )}
        htmlFor={`manager-${manager.id}`}
        title={managerFullName(manager)}
      >
        {managerShortName(manager)}
      </Label>
      {score && isDayOff && (
        <Badge
          variant="outline"
          className="text-[10px] px-1.5 py-0 text-muted-foreground"
        >
          ВЫХОДНОЙ
        </Badge>
      )}
      {!score && scoresLoading && (
        <>
          <div className="h-4 w-12 animate-pulse rounded-full bg-muted" />
          <div className="h-4 w-10 animate-pulse rounded-full bg-muted" />
        </>
      )}
      {score && !isDayOff && (
        <>
          {score.route_km_delta !== undefined && (
            <>
              {isBest && (
                <Star className="w-3 h-3 text-amber-400/60 fill-amber-400/60" />
              )}
              <Badge
                variant="outline"
                className={cn(
                  "text-[10px] px-1.5 py-0",
                  isBest && "border-green-500 text-green-700",
                )}
              >
                {score.route_km_delta === 0
                  ? "0 км"
                  : score.route_km_delta > MAX_BEST_ROUTE_KM_DELTA
                    ? `>${MAX_BEST_ROUTE_KM_DELTA} км`
                    : `+${score.route_km_delta.toFixed(1)} км`}
              </Badge>
            </>
          )}
          <Badge
            variant="secondary"
            className={cn(
              "text-[10px] px-1.5 py-0",
              selectedManagers.includes(manager.id) &&
                "border-green-500 text-green-700",
            )}
          >
            {selectedManagers.includes(manager.id)
              ? `${score.workload + 1} пл`
              : `${score.workload} пл`}
          </Badge>
        </>
      )}
    </div>
  );
};

interface ManagerRowCompactProps {
  manager: Manager;
  selectedManagers: string[];
  switchManager: (id: string) => void;
  isBest: boolean;
}

const ManagerRowCompact: FC<ManagerRowCompactProps> = ({
  manager,
  selectedManagers,
  switchManager,
  isBest,
}) => (
  <div className="flex items-center gap-2">
    <Checkbox
      id={`manager-${manager.id}`}
      onClick={() => switchManager(manager.id)}
      checked={selectedManagers.includes(manager.id)}
    />
    <span className="inline-flex items-center gap-1">
      <Label
        className="font-normal hover:cursor-pointer"
        htmlFor={`manager-${manager.id}`}
        title={managerFullName(manager)}
      >
        {managerShortName(manager)}
      </Label>
      {isBest && (
        <Star className="w-3 h-3 text-amber-400/60 fill-amber-400/60 flex-shrink-0" />
      )}
    </span>
  </div>
);

interface ManagerSectionProps {
  group: ManagerGroup;
  displayMode: ManagerDisplayMode;
  selectedManagers: string[];
  switchManager: (id: string) => void;
  scoreMap: Map<string, ManagerScore>;
  scoresLoading?: boolean;
}

const ManagerSection: FC<ManagerSectionProps> = ({
  group,
  displayMode,
  selectedManagers,
  switchManager,
  scoreMap,
  scoresLoading,
}) => {
  const isCompact = displayMode === "compact";
  const rowContainerClass =
    isCompact || group.label === "другие"
      ? "grid grid-cols-3 gap-2"
      : "flex flex-col gap-2";

  return (
    <div className="flex flex-col gap-2">
      <SectionLabel>{group.label}</SectionLabel>
      <div className={rowContainerClass}>
        {group.managers.map((manager) => {
          const score = scoreMap.get(manager.id);
          const isBest = manager.id === group.bestId;

          if (isCompact) {
            return (
              <ManagerRowCompact
                key={manager.id}
                manager={manager}
                selectedManagers={selectedManagers}
                switchManager={switchManager}
                isBest={isBest}
              />
            );
          }

          return (
            <ManagerRowDetailed
              key={manager.id}
              manager={manager}
              selectedManagers={selectedManagers}
              switchManager={switchManager}
              score={score}
              isBest={isBest}
              scoresLoading={scoresLoading}
            />
          );
        })}
      </div>
    </div>
  );
};

interface SelectManagersHeaderProps {
  displayMode: ManagerDisplayMode;
  onDisplayModeChange: (mode: ManagerDisplayMode) => void;
}

const SelectManagersHeader: FC<SelectManagersHeaderProps> = ({
  displayMode,
  onDisplayModeChange,
}) => (
  <div className="flex items-center gap-2">
    <Label>Менеджеры</Label>
    <Tabs
      value={displayMode}
      onValueChange={(v) => onDisplayModeChange(v as ManagerDisplayMode)}
    >
      <TabsList className="h-7">
        <TabsTrigger value="compact" className="h-6 w-6 p-0">
          <LayoutGrid className="h-3.5 w-3.5" />
        </TabsTrigger>
        <TabsTrigger value="detailed" className="h-6 w-6 p-0">
          <LayoutList className="h-3.5 w-3.5" />
        </TabsTrigger>
      </TabsList>
    </Tabs>
  </div>
);

const SelectManagers: FC<SelectManagersProps> = ({
  id,
  allManagers,
  switchManager,
  selectedManagers,
  scores,
  scoresLoading,
  displayMode: externalMode,
  onDisplayModeChange,
}) => {
  const [internalMode, setInternalMode] =
    useState<ManagerDisplayMode>("compact");

  const displayMode = externalMode ?? internalMode;

  const handleDisplayModeChange = useCallback(
    (mode: ManagerDisplayMode) => {
      setInternalMode(mode);
      onDisplayModeChange?.(mode);
    },
    [onDisplayModeChange],
  );

  const scoreMap = useMemo(
    () => new Map((scores ?? []).map((s) => [s.manager_id, s])),
    [scores],
  );

  const { drivers, withDepot, others } = useMemo(
    () => ({
      drivers: allManagers.filter((m) => m.is_driver),
      withDepot: allManagers.filter(
        (m) => !m.is_driver && m.depot_lat !== null,
      ),
      others: allManagers.filter((m) => !m.is_driver && m.depot_lat === null),
    }),
    [allManagers],
  );

  const groups: ManagerGroup[] = useMemo(() => {
    const bestInGroup = (group: Manager[]) => {
      const withScore = group.filter(
        (m) =>
          scoreMap.has(m.id) &&
          !scoreMap.get(m.id)!.is_day_off &&
          scoreMap.get(m.id)!.route_km_delta !== undefined,
      );
      if (!withScore.length) return null;
      const best = withScore.reduce((a, b) => {
        const da = scoreMap.get(a.id)!.route_km_delta!;
        const db = scoreMap.get(b.id)!.route_km_delta!;
        return da < db ? a : b;
      });
      if (scoreMap.get(best.id)!.route_km_delta! > MAX_BEST_ROUTE_KM_DELTA)
        return null;
      return best.id;
    };

    return [
      ...(withDepot.length > 0
        ? [
            {
              label: "с домом",
              managers: withDepot,
              bestId: bestInGroup(withDepot),
            },
          ]
        : []),
      ...(drivers.length > 0
        ? [
            {
              label: "водители",
              managers: drivers,
              bestId: bestInGroup(drivers),
            },
          ]
        : []),
      ...(others.length > 0
        ? [{ label: "другие", managers: others, bestId: null }]
        : []),
    ];
  }, [withDepot, drivers, others, scoreMap]);

  return (
    <div className="flex flex-col gap-3" id={id}>
      <SelectManagersHeader
        displayMode={displayMode}
        onDisplayModeChange={handleDisplayModeChange}
      />
      {groups.map((group) => (
        <ManagerSection
          key={group.label}
          group={group}
          displayMode={displayMode}
          selectedManagers={selectedManagers}
          switchManager={switchManager}
          scoreMap={scoreMap}
          scoresLoading={scoresLoading}
        />
      ))}
    </div>
  );
};

export default SelectManagers;
