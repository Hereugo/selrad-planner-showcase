import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Terminal } from "lucide-react";

const MaxDaysAlert = () => {
  return (
    <Alert variant={"warning"}>
      <Terminal className="h-4 w-4" />
      <AlertTitle>Внимание!</AlertTitle>
      <AlertDescription>
        Вы выбрали слишком длинный период дат. Пожалуйста, выберите период из не
        более 30 дней.
      </AlertDescription>
    </Alert>
  );
};

export default MaxDaysAlert;
