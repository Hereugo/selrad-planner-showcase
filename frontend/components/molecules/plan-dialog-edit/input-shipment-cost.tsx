import { TengeReciept } from "@/components/icons/tenge-reciept";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { FC } from "react";

interface ShipmentCostInputProps {
    id?: string;
    className?: string;
    shipmentCost: string;
    setShipmentCost: (cost: string) => void;
}

const ShipmentCostInput: FC<ShipmentCostInputProps> = ({ id, className, shipmentCost, setShipmentCost }) => {
    return (
        <div id={id} className={className}>
            <Label htmlFor="shipment_cost">Сумма отгрузки</Label>
            <div className="flex items-center text-muted-foreground hover:text-accent-foreground">
                <Input
                    value={shipmentCost}
                    onChange={(e) => {
                        if (e.target.value) {
                            if (e.target.value.match(/^[0-9]*\.?[0-9]{0,2}$/)) {
                                setShipmentCost(e.target.value)
                            }
                        } else {
                            setShipmentCost("0")
                        }
                    }}
                    type="text"
                    id="shipment_cost"
                    className="focus-visible:ring-0 hover:bg-accent"
                    autoComplete="off"
                    placeholder="0.00"
                />
                <TengeReciept className="-ml-8 h-4 w-4" />
            </div>
        </div>
    )
}

export default ShipmentCostInput;