#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, List

import pyrogram
from pyrogram import raw, types


class SendReaction:
    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        reaction: Union[List["types.ReactionType"], "types.ReactionType"] = [],
        is_big: bool = False,
        add_to_recent: bool = True
    ) -> "types.MessageReactions":
        """Use this method to change the chosen reactions on a message.
        Service messages can't be reacted to.
        Automatically forwarded messages from
        a channel to its discussion group have the
        same available reactions as messages in the channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.

            story_id (``int``, *optional*):
                Identifier of the story.

            reaction (List of :obj:`~pyrogram.types.ReactionType` *optional*):
                New list of reaction types to set on the message.
                Pass None as emoji (default) to retract the reaction.

            is_big (``bool``, *optional*):
                Pass True to set the reaction with a big animation.
                Defaults to False.
                
            add_to_recent (``bool``, *optional*):
                Pass True if the reaction should appear in the recently used reactions.
                This option is applicable only for users.

        Returns:
            :obj: `~pyrogram.types.MessageReactions`: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import ReactionTypeEmoji
                from pyrogram.raw.types import ReactionEmoji
                
                # Send a reaction one reaction
                await app.send_reaction(chat_id, message_id=message_id, reaction=[ReactionTypeEmoji(emoji="🔥")])
                
                # Send story reaction
                await app.send_reaction(chat_id, story_id=story_id, reaction=ReactionEmoji(emoji="🔥"))

                # Send multiple reaction as a premium user
                await app.send_reaction(chat_id, message_id=message_id, reaction=[ReactionTypeEmoji(emoji="👍"),ReactionTypeEmoji(emoji="😍")],True)

                # Retract a reaction
                await app.send_reaction(chat_id, message_id=message_id)
                await app.send_reaction(chat_id, story_id=story_id)
        """
        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=[
                        r.write(self)
                        for r in reaction
                    ] if reaction else [raw.types.ReactionEmpty()],
                    big=is_big,
                    add_to_recent=add_to_recent
                )
            )
            for i in r.updates:
              if isinstance(i, raw.types.UpdateMessageReactions):
                  return types.MessageReactions._parse(self, i.reactions)
        elif story_id is not None:
            await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=reaction if reaction else [raw.types.ReactionEmpty()],
                    add_to_recent=add_to_recent
                )
            )
            return True
        else:
            raise ValueError("You need to pass one of message_id!")