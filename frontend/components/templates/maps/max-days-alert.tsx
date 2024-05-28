import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { TriangleAlert } from "lucide-react";

const MaxDaysAlert = () => {
  return (
    <div className="absolute top-[50%] right-[50%] translate-x-[50%] -translate-y-[50%] z-50 w-96">
      <Alert variant={"warning"}>
        <TriangleAlert className="h-4 w-4" />
        <AlertTitle>Внимание!</AlertTitle>
        <AlertDescription>
          Вы выбрали слишком длинный период дат. Пожалуйста, выберите период из
          не более 30 дней.
        </AlertDescription>
      </Alert>
    </div>
  );
};

export default MaxDaysAlert;
