import { Textarea } from "@/components/ui/textarea";
import { FC } from "react";

interface CommentInputProps {
  id?: string;
  comment: string;
  setComment: (comment: string) => void;
}

const CommentInput: FC<CommentInputProps> = ({ id, comment, setComment }) => {
  return (
    <Textarea
      id={id}
      value={comment}
      onChange={(e) => setComment(e.target.value)}
      className="focus-visible:ring-0 hover:bg-accent hover:text-accent-foreground"
    />
  );
};

export default CommentInput;
