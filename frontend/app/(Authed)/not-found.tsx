import { Separator } from "@/components/ui/separator";

const NotFound = () => {
  return (
    <div className="flex flex-row items-center justify-center h-full gap-4">
      <span className="font-semibold text-2xl">404</span>
      <Separator orientation="vertical" className="h-12" />
      <span>Страница не найдена</span>
    </div>
  );
};

export default NotFound;
