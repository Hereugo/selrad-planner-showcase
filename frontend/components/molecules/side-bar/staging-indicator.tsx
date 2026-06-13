import { FC } from "react";
import { Badge } from "../../ui/badge";
import { FlaskConical } from "lucide-react";

const StagingIndicator: FC = () => {
  const isStaging = process.env.NEXT_PUBLIC_IS_STAGING === "true";

  if (!isStaging) {
    return null;
  }

  return (
    <Badge className="flex items-center gap-1.5 border-transparent bg-orange-500 text-white hover:bg-orange-500/80">
      <FlaskConical className="size-3" />
      <span>Тестовая среда</span>
    </Badge>
  );
};

export default StagingIndicator;
