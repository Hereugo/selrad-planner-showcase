import { TengeReciept } from "@/components/icons/tenge-reciept";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { parsePriceFormula } from "@/lib/utils";
import { FC } from "react";

interface ShipmentCostInputProps {
  id?: string;
  className?: string;
  shipmentCostFormula: string;
  setShipmentCostFormula: (costFormula: string) => void;
}

const ShipmentCostInput: FC<ShipmentCostInputProps> = ({
  id,
  className,
  shipmentCostFormula,
  setShipmentCostFormula,
}) => {
  return (
    <div id={id} className={className}>
      <Label htmlFor="shipment_cost">Сумма отгрузки</Label>
      <div className="flex items-center text-muted-foreground hover:text-accent-foreground">
        <Input
          value={shipmentCostFormula}
          onChange={(e) =>
            setShipmentCostFormula(parsePriceFormula(e.target.value))
          }
          type="text"
          id="shipment_cost"
          className="focus-visible:ring-0 hover:bg-accent"
          autoComplete="off"
          placeholder="0"
        />
        <TengeReciept className="-ml-8 h-4 w-4" />
      </div>
    </div>
  );
};

export default ShipmentCostInput;
