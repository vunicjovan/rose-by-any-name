from __future__ import annotations

import functools
import typing as t

import rio

from ..data_models import Book
from ..persistence import Persistence


@rio.page(
    name="CRUD",
    url_segment="",
)
class CrudPage(rio.Component):
    """
    A CRUD page that allows users to create, read, update, and delete book
    items.

    The @rio.event.on_populate decorator is used to fetch data from a predefined
    data model and assign it to the `book_items` attribute of the current
    instance.


    ### Attributes

    `book_items`: A list of book items.

    `currently_selected_book_item`: The currently selected book item.

    `banner_text`: The text to be displayed in the banner.

    `banner_style`: The style of the banner (success, danger, info).
    """

    book_items: list[Book] = []
    currently_selected_book_item: Book | None = None
    banner_text: str = ""
    banner_style: t.Literal["success", "danger", "info"] = "success"

    @rio.event.on_populate
    def on_populate(self) -> None:
        """
        Event handler that is called when the component is populated.

        Fetches data from a predefined data model and assigns it to the `book_items`
        attribute of the current instance.
        """

        self.book_items = self.session[Persistence].book_items

    async def on_press_delete_item(self, idx: int) -> None:
        """
        Perform actions when the "Delete" button is pressed.

        ## Parameters

        `idx`: The index of the item to be deleted.
        """

        # delete the item from the list
        self.book_items.pop(idx)
        self.banner_text = "Item was deleted"
        self.banner_style = "danger"
        self.currently_selected_book_item = None

    async def _create_dialog_item_editor(
        self,
        selected_item: Book,
        new_entry: bool,
    ) -> Book | None:
        """
        Creates a dialog to edit or add a book item.

        This method creates a dialog that allows the user to edit or add a book
        item. The dialog contains input fields for the name, description, price,
        and category of the book item. The user can save or cancel the changes.
        If the user saves the changes, the updated book item is returned. If the
        user cancels the changes, the original book item is returned.

        ### Parameters

        `selected_item`: The selected item to be edited or added.

        `new_entry`: A boolean flag indicating if the item is a new entry.
        """

        # Make a copy of the selected item to avoid modifying the original,
        # which is returned if the user cancels the dialog.
        selected_item_copied = selected_item.copy()

        # This function will be called to create the dialog's content.
        # It builds up a UI using Rio components, just like a regular
        # `build` function would.
        def build_dialog_content() -> rio.Component:
            # Build the dialog
            if new_entry is False:
                text = "Edit Item"
            else:
                text = "Add New Item"

            return rio.Column(
                rio.Text(
                    text=text,
                    style="heading2",
                    margin_bottom=1,
                ),
                rio.TextInput(
                    selected_item_copied.title,
                    label="Title",
                    on_change=on_change_title,
                ),
                rio.TextInput(
                    selected_item_copied.author,
                    label="Author",
                    on_change=on_change_author,
                ),
                rio.NumberInput(
                    selected_item_copied.publishing_year,
                    label="Publishing Year",
                    on_change=on_change_publishing_year,
                ),
                rio.NumberInput(
                    selected_item_copied.number_of_pages,
                    label="Number of Pages",
                    on_change=on_change_number_of_pages,
                ),
                rio.Row(
                    rio.Button(
                        "Save",
                        on_press=lambda selected_book_item_copied=selected_item_copied: dialog.close(
                            selected_book_item_copied
                        ),
                    ),
                    rio.Button(
                        "Cancel",
                        on_press=lambda: dialog.close(None),
                        style="minor",
                        color="danger",
                    ),
                    spacing=1,
                    align_x=1,
                ),
                spacing=1,
                align_y=0,
                align_x=0.5,
            )

        def on_change_title(ev: rio.TextInputChangeEvent) -> None:
            """
            Changes the title of the currently selected book. And updates the
            title attribute of our data model.

            ## Parameters

            `ev`: The event object that contains the new title.
            """

            selected_item_copied.title = ev.text

        def on_change_author(ev: rio.TextInputChangeEvent) -> None:
            """
            Changes the author of the currently selected book. And updates the
            author attribute of our data model.

            ## Parameters

            `ev`: The event object that contains the new author.
            """

            selected_item_copied.author = ev.text

        def on_change_publishing_year(ev: rio.NumberInputChangeEvent) -> None:
            """
            Changes the publishing year of the currently selected book. And updates the
            publishing_year attribute of our data model.

            ## Parameters

            `ev`: The event object that contains the new publishing year.
            """

            selected_item_copied.publishing_year = int(ev.value)

        def on_change_number_of_pages(ev: rio.NumberInputChangeEvent) -> None:
            """
            Changes the number of pages of the currently selected book. And updates the
            number_of_pages attribute of our data model.

            ## Parameters

            `ev`: The event object that contains the new number of pages.
            """

            selected_item_copied.number_of_pages = int(ev.value)

        # Show the dialog
        dialog = await self.session.show_custom_dialog(
            build=build_dialog_content,
            # Prevent the user from interacting with the rest of the app
            # while the dialog is open
            modal=True,
            # Don't close the dialog if the user clicks outside of it
            user_closable=False,
        )

        # Wait for the user to select an option
        result = await dialog.wait_for_close()

        # Return the selected value
        return result

    async def on_spawn_dialog_edit_book_item(
        self,
        selected_item: Book,
        idx: int,
    ) -> None:
        """
        Opens a dialog to edit the selected book item.

        Updates the book item at the given index if the user confirms the changes.

        ### Parameters

        `selected_book_item`: The selected book item to be edited.

        `idx`: The index of the selected book item in the list of book items.
        """

        assert selected_item is not None
        result = await self._create_dialog_item_editor(
            selected_item=selected_item,
            new_entry=False,
        )

        # Ensure the result is not None
        if result is None:
            self.banner_text = "Item was NOT updated"
            self.banner_style = "danger"
        else:
            # Update the book item
            self.book_items[idx] = result
            self.banner_text = "Item was updated"
            self.banner_style = "info"

    async def on_spawn_dialog_add_new_book_item(self) -> None:
        """
        Perform actions when the "Add New" ListItem is pressed.

        This method creates a new empty book item of models.Book.
        It then opens a dialog for the user to enter the details of the
        new book item. If the user confirms the addition and the new
        book item is not empty, it appends the new book item to the list
        of book items and updates the banner text accordingly.

        If the user cancels the addition or the new book item is empty,
        it updates the banner text to indicate that the item was not added.
        """

        new_book_item = Book.new_empty()
        result = await self._create_dialog_item_editor(
            selected_item=new_book_item,
            new_entry=True,
        )

        # Ensure the result is not None
        if result is None:
            self.banner_text = "Item was NOT updated"
            self.banner_style = "danger"
        else:
            # Append the new book item to our list of book items only
            # if it is not empty
            if result != Book.new_empty():
                self.book_items.append(result)
                self.banner_text = "Item was added"
                self.banner_style = "success"
            else:
                self.banner_text = "Item was NOT added"
                self.banner_style = "danger"

    def build(self) -> rio.Component:
        """
        Builds the component to be rendered.

        If there is no currently selected book item, only the Banner and
        ItemList component is returned.

        When you click on a SimpleListItem, a custom Dialog appears, allowing
        you to edit the selected item. Similarly, clicking on the "Add new"
        SimpleListItem opens a custom Dialog for adding a new item.
        """

        # Store all children in an intermediate list
        list_items = []

        list_items.append(
            rio.SimpleListItem(
                text="Add new",
                secondary_text="Description",
                key="add_new",
                left_child=rio.Icon("material/add"),
                on_press=self.on_spawn_dialog_add_new_book_item,
            )
        )

        for i, item in enumerate(self.book_items):
            list_items.append(
                rio.SimpleListItem(
                    text=item.title,
                    secondary_text=item.author,
                    right_child=rio.Button(
                        rio.Icon("material/delete", margin=0.5),
                        color=self.session.theme.danger_color,
                        # Center button vertically so it doesn't blow up on
                        # smaller screens.
                        align_y=0.5,
                        # Adjust button size based on window width. Smaller
                        # buttons for smaller screens.
                        min_width=8 if self.session.window_width > 60 else 4,
                        # Note the use of functools.partial to pass the
                        # index to the event handler.
                        on_press=functools.partial(self.on_press_delete_item, i),
                    ),
                    # Use the title as the key to ensure that the list item
                    # is unique.
                    key=item.title,
                    # Note the use of functools.partial to pass the
                    # item to the event handler.
                    on_press=functools.partial(
                        self.on_spawn_dialog_edit_book_item,
                        item,
                        i,
                    ),
                )
            )

        # Then unpack the list to pass the children to the ListView
        return rio.Column(
            rio.Banner(
                self.banner_text,
                style=self.banner_style,
                margin_bottom=1,
            ),
            rio.ListView(
                *list_items,
                align_y=0,
            ),
            # align at the top
            align_y=0,
            margin=3,
        )
