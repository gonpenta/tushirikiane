import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { I_CreatCardInput, I_EditCardInput } from "../interfaces/inputs";
import {
  I_GetCardRespone as I_CreateCardResponse,
  I_EditCardResponse,
  I_GetCardRespone,
} from "../interfaces/responses";
import { protectedApi } from "../kyInstance";
import { QUERY_KEYS } from "../queryKeys";
import { URLS } from "../urls";

export const useCreateCard = (
  workSpaceId: string,
  boardId: string,
  listId: string,
  onSuccess?: () => void,
  onError?: () => void
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (
      values: I_CreatCardInput
    ): Promise<I_CreateCardResponse> => {
      return await protectedApi
        .post(URLS.apiCards(workSpaceId, boardId, listId), { json: values })
        .json();
    },
    onSuccess: (createdCard) => {
      queryClient.setQueryData<I_GetCardRespone[]>(
        [QUERY_KEYS.cards(workSpaceId, boardId, listId)],
        (oldCards = []) => [...oldCards, createdCard]
      );
      toast.success("Card created successfully.");
      onSuccess?.();
    },
    onError: (error) => {
      console.error("Error creating card", error);
      toast.error("Failed to create card. Please try again");
      onError?.();
    },
  });
};

export const useEditCard = (
  workSpaceId: string,
  boardId: string,
  listId: string,
  cardId: string,
  onSuccess?: () => void,
  onError?: () => void
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (
      values: I_EditCardInput
    ): Promise<I_EditCardResponse> => {
      return await protectedApi
        .put(URLS.apiCardsDetail(workSpaceId, boardId, listId, cardId), {
          json: values,
        })
        .json();
    },
    onSuccess: (editedCard) => {
      queryClient.setQueryData<I_GetCardRespone[]>(
        [QUERY_KEYS.cards(workSpaceId, boardId, listId)],
        (oldCards = []) =>
          oldCards.map((card) =>
            card.id === editedCard.id ? editedCard : card
          )
      );

      toast.success("Card updated successfully.");
      onSuccess?.();
    },
    onError: (error) => {
      console.error("Error updating card", error);
      toast.error("Failed to update card. Please try again");
      onError?.();
    },
  });
};
