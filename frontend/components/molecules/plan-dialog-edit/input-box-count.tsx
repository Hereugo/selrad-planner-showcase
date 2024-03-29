import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { PackageOpen } from "lucide-react";
import { FC } from "react";

interface BoxCountInputProps {
    id?: string;
    className?: string;
    boxCount: string;
    setBoxCount: (count: string) => void;
}

const BoxCountInput: FC<BoxCountInputProps> = ({ id, className, boxCount, setBoxCount }) => {
    return (
        <div id={id} className={className}>
            <Label htmlFor="box_count">Количество коробок</Label>
            <div className="flex items-center text-muted-foreground hover:text-accent-foreground">
                <Input
                    value={boxCount}
                    onChange={(e) => {
                        if (e.target.value) {
                            setBoxCount(e.target.value)
                        } else {
                            setBoxCount("0")
                        }
                    }}
                    type="text"
                    id="box_count"
                    className="focus-visible:ring-0 hover:bg-accent"
                    autoComplete="off"
                    placeholder="0"
                />
                <PackageOpen className="-ml-8 h-4 w-4" />
            </div>
        </div>
    )
}

export default BoxCountInput;