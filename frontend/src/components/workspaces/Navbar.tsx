"use client";

import { URLS } from "@/lib/urls";
import { BoardsProvider, useBoards } from "@/providers/BoardsProvider";
import { useWorkSpaces } from "@/providers/WorkSpacesProvider";
import { Button, Group, Menu, Skeleton, Stack, Text } from "@mantine/core";
import {
  IconCalendar,
  IconChevronDown,
  IconHome,
  IconLayout,
  IconListCheck,
  IconUsers,
} from "@tabler/icons-react";
import Link from "next/link";
import { useParams, usePathname } from "next/navigation";
import CreateBoardButton from "../boards/CreateBoardButton";
import DeleteWorkSpaceButton from "./DeleteWorkSpaceButton";
import InviteToWorkSpaceButton from "./InviteToWorkSpaceButton";

const mainMenuItems = [
  { icon: <IconHome size={18} />, label: "Home", href: URLS.workspaces },
  { icon: <IconListCheck size={18} />, label: "Tasks", href: URLS.tasks },
  { icon: <IconCalendar size={18} />, label: "Calendar", href: URLS.calendar },
  { icon: <IconUsers size={18} />, label: "Team", href: URLS.team },
];

const Navbar = () => {
  const pathname = usePathname();

  return (
    <Stack>
      <WorkSpacesMenu />
      {/* <WorkspaceMainMenuCard /> */}
      {pathname.startsWith("/workspaces/") && (
        <BoardsProvider>
          <WorkspaceBoards />
        </BoardsProvider>
      )}
    </Stack>
  );
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const WorkspaceMainMenuCard = () => {
  const pathname = usePathname();

  return (
    <Stack>
      <Text size="xs">MAIN MENU</Text>
      {mainMenuItems.map((item, index) => {
        const isActive = pathname === item.href;

        return (
          <Button
            key={index}
            component={Link}
            href={item.href}
            variant={isActive ? "filled" : "light"}
            fullWidth
            justify="start"
            leftSection={item.icon}
          >
            <Text fw={isActive ? 700 : 400}>{item.label}</Text>
          </Button>
        );
      })}
    </Stack>
  );
};

const WorkSpacesMenu = () => {
  const { data: workSpaces, isLoading } = useWorkSpaces();

  const { workSpacesSlug } = useParams<{
    workSpacesSlug: string;
    boardsSlug: string;
  }>();

  const activeWorkSpace = workSpaces?.find(
    (workSpace) => workSpace?.id === workSpacesSlug
  );

  return (
    <Group align="center">
      <Menu shadow="md" disabled={isLoading} withArrow>
        <Menu.Target>
          <Button
            variant="light"
            flex={1}
            disabled={isLoading}
            rightSection={<IconChevronDown size={16} />}
          >
            {workSpacesSlug && activeWorkSpace
              ? activeWorkSpace.name
              : "Workspaces"}
          </Button>
        </Menu.Target>

        <Menu.Dropdown p="xs">
          {isLoading
            ? Array.from({ length: 5 }).map((_, index) => (
                <Menu.Item key={index}>
                  <Skeleton height={20} radius="sm" />
                </Menu.Item>
              ))
            : workSpaces?.map((workSpace) => {
                const isActive = workSpacesSlug === workSpace?.id;

                return (
                  <Menu.Item
                    key={workSpace?.id}
                    component={Link}
                    href={URLS.workspacesSlug(workSpace.id)}
                    style={{
                      fontWeight: isActive ? 600 : 400,
                      backgroundColor: isActive ? "#f1f3f5" : "transparent",
                    }}
                  >
                    {workSpace.name}
                  </Menu.Item>
                );
              })}
        </Menu.Dropdown>
      </Menu>

      <DeleteWorkSpaceButton />
      <InviteToWorkSpaceButton />
    </Group>
  );
};

const WorkspaceBoards = () => {
  const { workSpacesSlug, boardsSlug } = useParams<{
    workSpacesSlug: string;
    boardsSlug: string;
  }>();

  const { data: boards, isLoading } = useBoards();

  return (
    <Stack>
      <Group justify="space-between">
        <Text size="xs">BOARDS</Text>
        <CreateBoardButton />
      </Group>

      {isLoading ? (
        Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} height={36} radius="sm">
            <Button
              variant="light"
              fullWidth
              justify="start"
              leftSection={<IconLayout />}
              disabled
            >
              <Text>Loading...</Text>
            </Button>
          </Skeleton>
        ))
      ) : boards?.length === 0 ? (
        <Text size="sm" ta="center" c="dimmed" mt="sm">
          No boards found. Create one to get started.
        </Text>
      ) : (
        boards?.map((board) => {
          const isActive = boardsSlug === board?.slug;

          return (
            <Group key={board.id} gap="xs">
              <Button
                component={Link}
                href={URLS.boardsSlug(workSpacesSlug, board?.id)}
                variant={isActive ? "filled" : "light"}
                fullWidth
                justify="start"
                leftSection={<IconLayout />}
                flex={1}
              >
                <Text fw={isActive ? 700 : 400}>{board.name}</Text>
              </Button>
            </Group>
          );
        })
      )}
    </Stack>
  );
};

export default Navbar;
