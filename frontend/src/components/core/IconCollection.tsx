import {
  IconDotsVertical,
  IconEdit,
  IconPinnedFilled,
  IconPlus,
  IconShare,
  IconTrash,
  IconUsers,
  IconX,
} from "@tabler/icons-react";

interface IconProps {
  size?: number;
  stroke?: number;
  color?: string;
}

export const IconCollection = {
  Delete: ({ size = 24, stroke = 1.5 }: IconProps) => (
    <IconTrash size={size} stroke={stroke} color={"red"} />
  ),
  Create: ({ size = 24, stroke = 1.5, color = "currentColor" }: IconProps) => (
    <IconPlus size={size} stroke={stroke} color={color} />
  ),
  Edit: ({ size = 24, stroke = 1.5, color = "currentColor" }: IconProps) => (
    <IconEdit size={size} stroke={stroke} color={color} />
  ),
  Close: ({ size = 24, stroke = 1.5, color = "red" }: IconProps) => (
    <IconX size={size} stroke={stroke} color={color} />
  ),
  Actions: ({ size = 24, stroke = 1.5, color = "currentColor" }: IconProps) => (
    <IconDotsVertical size={size} stroke={stroke} color={color} />
  ),
  Share: ({ size = 24, stroke = 1.5, color = "currentColor" }: IconProps) => (
    <IconShare size={size} stroke={stroke} color={color} />
  ),
  Assign: ({ size = 24, stroke = 1.5, color = "currentColor" }: IconProps) => (
    <IconUsers size={size} stroke={stroke} color={color} />
  ),
  Assigned: ({
    size = 24,
    stroke = 1.5,
    color = "currentColor",
  }: IconProps) => (
    <IconPinnedFilled size={size} stroke={stroke} color={color} />
  ),
};
