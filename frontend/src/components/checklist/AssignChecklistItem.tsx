"use client";

import { I_GetChecklistItemResponse } from "@/lib/interfaces/responses";
import {
  useAssignChecklistItem,
  useUnassignChecklistItem,
} from "@/lib/mutations/checklists";
import { useGetBoardMembers } from "@/lib/queries/boards";
import {
  ActionIcon,
  Group,
  Menu,
  ScrollArea,
  Stack,
  Text,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useParams } from "next/navigation";
import React from "react";
import { IconCollection } from "../core/IconCollection";
import MemberAvatar from "../core/MemberAvatar";

interface AssignChecklistItemProps extends I_GetChecklistItemResponse {
  listId: string;
}

const AssignChecklistItem: React.FC<AssignChecklistItemProps> = ({
  listId,
  task_id,
  assignee_id,
  id,
}) => {
  const { workSpacesSlug, boardsSlug } = useParams<{
    workSpacesSlug: string;
    boardsSlug: string;
  }>();

  const [opened, { open, close }] = useDisclosure(false);

  const { data: boardMembers } = useGetBoardMembers(workSpacesSlug, boardsSlug);

  const { mutate: assignChecklistItem, isPending } = useAssignChecklistItem(
    workSpacesSlug,
    boardsSlug,
    listId,
    task_id,
    id
  );

  const {
    mutate: unassignChecklistItem,
    isPending: isPendingUnassignChecklistItem,
  } = useUnassignChecklistItem(workSpacesSlug, boardsSlug, listId, task_id, id);

  const handleOnAssignClick = (userId: string) => {
    assignChecklistItem({ assignee_id: userId });
  };

  const handleOnUnassignClick = () => {
    unassignChecklistItem();
  };

  return (
    <Menu shadow="md" width={220} opened={opened} onClose={close}>
      <Menu.Target>
        <ActionIcon
          onClick={open}
          loading={isPending || isPendingUnassignChecklistItem}
        >
          <IconCollection.Assign />
        </ActionIcon>
      </Menu.Target>

      <Menu.Dropdown>
        <ScrollArea.Autosize mah={300} type="scroll">
          
          {boardMembers?.map((p, index) => {
            return (
              <Menu.Item
                key={index}
                onClick={
                  p.member.id === assignee_id
                    ? handleOnUnassignClick
                    : () => handleOnAssignClick(p.member.id)
                }
                leftSection={
                  <Group align="center" justify="center">
                    {p.member.id === assignee_id && (
                      <IconCollection.Assigned size={16} color="blue" />
                    )}
                  </Group>
                }
              >
                <Group align="center">
                  <MemberAvatar
                    fullName={`${p.member.first_name} ${p.member.last_name}`}
                    initials={
                      p.member.first_name.charAt(0).toUpperCase() +
                      (p.member.last_name.charAt(0)?.toUpperCase() || "")
                    }
                  />
                  <Stack>
                    <Text fw={500} size="sm" truncate>
                      {`${p.member.first_name} ${p.member.last_name}`}
                    </Text>
                  </Stack>
                </Group>
              </Menu.Item>
            );
          })}
        </ScrollArea.Autosize>
      </Menu.Dropdown>
    </Menu>
  );
};

export default AssignChecklistItem;
