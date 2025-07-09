import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleDDYearSelection(self, e):
        pass

    def fillDDStore(self):
        try:
            stores = self._model.getStores()
            self._view._ddStore.options.clear()
            #self._view._ddStore.on_change = self._fillYears
            for store in stores:
                self._view._ddStore.options.append(
                    ft.dropdown.Option(key = f"{store.store_id}-{store.store_name}",
                                       data = store,
                                       on_click=self._fillYears))
            self._view.update_page()
        except Exception as ex:
            self._show_error(f"Errore caricamento store: {ex}")

    def _fillYears(self, e):
        store = e.control.data
        print(e.control.data)
        years = self._model.getYearsByStores(store.store_id)
        for year in years:
            self._view._ddYear.options.append(
                ft.dropdown.Option(f"{year}")
            )
        self._view.update_page()


    def handleCreaGrafo(self, e):
        try:
            # reset area messaggi
            self._view._txt_result.controls.clear()

            if not self._view._ddStore.value:
                raise ValueError("Devi selezionare uno store.")
            k_str = self._view._txtIntK.value or ""
            if not k_str.isdigit():
                raise ValueError("K deve essere un intero positivo.")
            kint = int(k_str)
            year = self._view._ddYear.value
            #anno facoltativo, ma se presente deve essere intero 2016–2018
            year_str = (self._view._ddYear.value or "").strip()
            if year_str:
                if not year_str.isdigit():
                    raise ValueError("L'anno deve essere un numero intero.")
                year = int(year_str)
                if year < 2016 or year > 2018:
                    raise ValueError("L'anno deve essere compreso tra 2016 e 2018.")
            else:
                year = None


            self._model.buildGraph(self._view._ddStore.value[0], kint, year)

            allNodes = self._model.getAllNodes()
            self.fillDDNodes(allNodes)

            Nnodes, Nedges = self._model.getGraphDetails()
            self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {Nnodes}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {Nedges}"))
            self._view.update_page()

        except Exception as ex:
            self._show_error(f"Errore creazione grafo: {ex}")

    def handleCerca(self, e):
        try:
            self._view._txt_result.controls.clear()
            if not self._view._ddNode.value:
                raise ValueError("Devi selezionare un nodo di partenza.")
            print(self._view._ddNode.value[0])
            nodes = self._model.getCammino(self._view._ddNode.value[0])
            self._view._txt_result.controls.append(ft.Text(f"Nodo di partenza: {self._view._ddNode.value}"))
            for n in nodes:
                self._view._txt_result.controls.append(ft.Text(str(n)))
            self._view.update_page()

        except Exception as ex:
            self._show_error(f"Errore ricerca cammino: {ex}")

    def fillDDNodes(self, allNodes):
        try:
            self._view._ddNode.options.clear()
            for n in allNodes:
                print(n)
                self._view._ddNode.options.append(ft.dropdown.Option(
                    text=f"{n.product_id}-{n.product_name}",
                    data = n,
                    on_click= self._DDNodes
                ))
            self._view.update_page()
        except Exception as ex:
            self._show_error(f"Errore popolamento nodi: {ex}")

    def _DDNodes(self, e):
        if e.control.data is None:
            self._selectedNode = None
        else:
            self._selectedNode = e.control.data


    def handleRicorsione(self, e):
        pass

    def _show_error(self, message: str):
        """Mostra un messaggio di errore in txt_result."""
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(message, color="red"))
        self._view.update_page()