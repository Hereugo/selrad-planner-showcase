import { Textarea } from "@/components/ui/textarea";
import { FC } from "react";

interface CommentInputProps {
  id?: string;
  setComment: (comment: string) => void;
}

const CommentInput: FC<CommentInputProps> = ({ id, setComment }) => {
  return (
    <Textarea
      id={id}
      onChange={(e) => setComment(e.target.value)}
      className="focus-visible:ring-0 hover:bg-accent hover:text-accent-foreground"
    />
  );
};

export default CommentInput;
