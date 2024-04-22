"use client";

import { Button } from "@/components/ui/button";
import { FC } from "react";
import { useDownloadExcel } from "./index.hooks";

interface ExportExcelTemplateProps {}

const ExportExcelTemplate: FC<ExportExcelTemplateProps> = () => {
  const { handleDownload } = useDownloadExcel();

  return (
    <>
      <Button onClick={handleDownload} className="w-full">
        Скачать
      </Button>
    </>
  );
};

export default ExportExcelTemplate;
