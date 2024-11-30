import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import PlanDialog from "../plan-dialog-new";
import { FC } from "react";
import { cn } from "@/lib/utils";
import { useViewFeature } from "@/lib/hooks/useViewFeature";

interface NewPlanButtonProps {
  className?: string;
}

const NewPlanButton: FC<NewPlanButtonProps> = ({ className }) => {
  return (
    <PlanDialog>
      <Button className={cn("w-full flex gap-2 justify-start px-2", className)}>
        <Plus />
        Создать план
      </Button>
    </PlanDialog>
  );
};

export default NewPlanButton;
