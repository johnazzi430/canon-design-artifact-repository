<template>
    <div>
      <button type="button"
              class="btn btn-default"
              @click="getSelectedRows()">Get Selected Rows
            </button>
      <ag-grid-vue style="width: 100%; height: 500px;"
                   class="ag-theme-balham"
                   :columnDefs="columnDefs"
                   :rowData="rowData"
                   :modules="modules"
                   rowSelection="single"
                   @grid-ready="onGridReady">
      </ag-grid-vue>
    </div>
</template>

<script>
/*eslint-disable */
    import {AgGridVue} from "@ag-grid-community/vue";
    import {AllCommunityModules} from '@ag-grid-community/all-modules';

    export default {
        name: 'App',
        data() {
            return {
                columnDefs: null,
                rowData: null,
                rowSelection: null,
                gridApi: null,
                gridOptions: null,
                modules: AllCommunityModules
            }
        },
        components: {
            AgGridVue
        },
        methods: {
                    onGridReady(params) {
                        this.gridApi = params.api;
                        this.columnApi = params.columnApi;
                    },
                    getSelectedRows() {
                        const selectedNodes = this.gridApi.getSelectedNodes();
                        const selectedData = selectedNodes.map( node => node.data );
                        const selectedDataStringPresentation = selectedData.map( node => node.make + ' ' + node.model).join(', ');
                        alert(`Selected nodes: ${selectedDataStringPresentation}`);
                    }
                },
        beforeMount() {
          this.columnDefs = [
            {headerName: "Name", field: "name"},
            {headerName: "Title", field: "title"},
            {headerName: "Quote", field: "quote"},
            {headerName: "Function", field: "function"},
            {headerName: "Qty", field: "qty"},
            {headerName: "Internal or External", field: "External"}
          ];
          this.rowSelection = "single";

          fetch('http://localhost:5000/api/persona_table')
                          .then(result => result.json())
                          .then(rowData => this.rowData = rowData);
        },
    }
</script>

<style>
</style>
