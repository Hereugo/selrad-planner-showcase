import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

const NewPlanButton = () => {
    return (
        <Button className="w-full flex gap-2 justify-start px-2">
            <Plus />
            Создать план
        </Button>
    )
}

export default NewPlanButton;