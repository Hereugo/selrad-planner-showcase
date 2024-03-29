import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import PlanDialog from "../plan-dialog-new";

const NewPlanButton = () => {
  return (
    <PlanDialog>
      <Button className="w-full flex gap-2 justify-start px-2">
        <Plus />
        Создать план
      </Button>
    </PlanDialog>
  );
};

export default NewPlanButton;
