<script>
import Cortex from "./components/Cortex.vue";
import Panel from "./components/Panel.vue";
import "ant-design-vue/dist/antd.css";
import { message } from "ant-design-vue";
import _ from "lodash";
const urlSearch = location.search.slice(1);
const urlParams = urlSearch
  ? Object.fromEntries(urlSearch.split("&").map((item) => item.split("=")))
  : {};
var ws = new WebSocket(
  "ws://localhost:8888",
  `h5_${urlSearch.replace(/=/g, "")}`
);
// var ws = new WebSocket("ws://192.168.123.244:8888", `h5_${urlSearch.replace(/=/g, '')}`);
window.region = {};
window.message = message;
message.config({
  maxCount: 1,
});
export default {
  name: "app",
  data() {
    return {
      fileData: {
        allFileName: [],
        somas: {},
        soma_pos: [],
        dendrites: [],
        dendrite_pos: [],
        nerves: {},
        marker: [],
        region: {},
        region_range: {},
        consts: {},
        nerve_props_keys_map: {},
      },
      allFileName: [],
      somas: [],
      soma_pos: [],
      dendrites: [],
      dendrite_pos: [],
      nerves: [],
      marker: [],
      region: {},
      region_range: {},
      consts: {},
      nerve_props_keys_map: {},
      options: this.getOptionStore(),
      consts: {
        nerveType: {
          soma: 0,
          axon: 1,
          axonEnd: 2,
          dendrite: 3,
          dendrite_nor: 4,
        },
      },
      viewPortRange: this.getViewPortRange(),
      appMode: "view", // edit view
      allFormProcess: [],
      allGrayMaskPath: [],
      hoverSomaName: "",
    };
  },
  computed: {
    historyFiles() {
      const { onlyShowHistoryFileNames = [], historyFileNamesRegStr = "" } =
        this.options;
      const historyFileNamesReg = RegExp(historyFileNamesRegStr);
      return this.allFileName.filter((name) => {
        if (
          (!onlyShowHistoryFileNames.length ||
            onlyShowHistoryFileNames.includes(name.split(";")[1])) &&
          (!historyFileNamesRegStr || historyFileNamesReg.test(name))
        ) {
          return true;
        } else {
          return false;
        }
      });
    },
  },
  mounted() {
    this.listenWs();
    setTimeout(() => {
      this.sendReadFileReq("init");
    }, 500);
    this.listenMenu();
    this.listenScrollEnd(this.updateViewPortOnScrollEnd);
  },
  render() {
    const { padding = {} } = this.fileData.consts;
    return (
      <div id="main-container" ref="app">
        <Cortex
          appMode={this.appMode}
          marker={this.fileData.marker}
          regionRange={this.fileData.region_range}
          options={this.options}
          updateOptions={this.updateOptions.bind(this)}
          cortexConsts={this.fileData.consts}
          nervePropsKeysMap={this.fileData.nerve_props_keys_map}
          somas={this.fileData.somas}
          somaPos={this.fileData.soma_pos}
          dendrites={this.fileData.dendrites}
          dendritePos={this.fileData.dendrite_pos}
          nerves={this.fileData.nerves}
          nervePos={this.fileData.nerve_pos}
          nerveType={this.consts.nerveType}
          getViewPortRange={this.getViewPortRange}
          addConnect={this.addConnect}
          allFormProcess={this.fileData.allFormProcess}
          requireSomaName={this.requireSomaName.bind(this)}
          hoverSomaName={this.hoverSomaName}
        />
        <Panel
          appMode={this.appMode}
          showPanel={this.showPanel.bind(this)}
          visible={this.options.panelShow}
          somas={this.fileData.somas}
          dendrites={this.fileData.dendrites}
          nerves={this.fileData.nerves}
          cortexConsts={this.fileData.consts}
          searchNerveResult={this.fileData.search_nerve_result}
          options={this.options}
          updateOptions={this.updateOptions.bind(this)}
          allFileName={this.allFileName}
          setReadFileName={this.setReadFileName.bind(this)}
          gotoElevator={this.gotoElevator.bind(this)}
          highlightStaticPart={this.highlightStaticPart.bind(this)}
          nervePropsKeysMap={this.fileData.nerve_props_keys_map}
          addNewRegion={this.addNewRegion.bind(this)}
          deleteRegion={this.deleteRegion.bind(this)}
          addRegionNeuron={this.addRegionNeuron.bind(this)}
          deleteRegionNeuron={this.deleteRegionNeuron.bind(this)}
          addFormProcess={this.addFormProcess.bind(this)}
          allFormProcess={this.fileData.allFormProcess}
          getPartProp={Cortex.getPartProp}
          updateConnection={this.updateConnection.bind(this)}
          updateRegion={this.updateRegion.bind(this)}
          saveRegion={this.saveRegion.bind(this)}
          allGrayMaskPath={this.fileData.allGrayMaskPath}
          modifyConnect={this.modifyConnect.bind(this)}
          changeRegionOffsetX={this.changeRegionOffsetX.bind(this)}
          changeRegionHighlightNeuronRegExp={this.changeRegionHighlightNeuronRegExp.bind(
            this
          )}
        />
      </div>
    );
  },
  methods: {
    listenWs() {
      ws.onmessage = ((event) => {
        const EVENT_OBJ = JSON.parse(event.data || "{}");
        const { type, data: fileData } = EVENT_OBJ;
        switch (type) {
          case "readFileRes":
            console.log("[readFileRes]");
            message.success(`read succ：${fileData.nerves.type.length}`);
            if (fileData.allFileName) {
              this.allFileName = fileData.allFileName;
            }

            if (fileData.region) {
              window.region = fileData.region;
              delete fileData.region;
            }

            this.fileData = {
              ...this.fileData,
              ...fileData,
            };

            this.updateOptions(
              {
                readFileName: fileData.fileName,
              },
              false
            );

            setTimeout(() => {
              // this.autoNextFileName();
            }, 10);

            // if (fileData.stage === "init") {
            // const elevatorRegion = this.options.elevatorRegion;
            // setTimeout(() => {
            //   this.gotoElevator(
            //     elevatorRegion,
            //     this.options.elevatorAnchor[elevatorRegion]
            //   );
            // }, 0);
            // }
            break;
          case "readFileResErr":
            message.warn(fileData.message);
            break;
          case "copy_connection":
            this.copyText(fileData);
            break;
          case "modify_connect":
            if (fileData.success === true) {
              message.success("save succ");
            } else {
              message.success("save fail");
            }
            break;
          case "require_soma_name_res":
            this.hoverSomaName = fileData;
        }
      }).bind(this);
    },
    autoNextFileName() {
      const curFileInd = this.historyFiles.findIndex(
        (fileName) => fileName === this.options.readFileName
      );
      console.log("[autoNextFileName]", curFileInd);
      if (curFileInd > -1 && curFileInd < this.historyFiles.length - 1) {
        this.setReadFileName(this.historyFiles[curFileInd + 1]);
      }
    },
    listenMenu() {
      document.addEventListener("contextmenu", this.onContextmenu.bind(this));
    },
    copyText(text) {
      let textarea = document.createElement("textarea");
      textarea.style.position = "fixed";
      const currentFocus = document.activeElement;
      document.body.appendChild(textarea);
      textarea.value = text;
      textarea.focus();
      textarea.setSelectionRange(0, textarea.value.length);
      document.execCommand("copy");
      document.body.removeChild(textarea);
      currentFocus.focus();
      message.success("copy succ");
    },
    setReadFileName(readFileName) {
      this.updateOptions({ readFileName });
    },
    gotoElevator(regionName, newRowNColNo) {
      if (newRowNColNo) {
        const newElevatorAnchor = {
          ...this.options.elevatorAnchor,
          ...{ [regionName]: newRowNColNo },
        };
        this.updateOptions(
          {
            elevatorRegion: regionName,
            elevatorAnchor: newElevatorAnchor,
          },
          false
        );
        const region_range = this.fileData.region_range[regionName];
        const x =
          region_range["x_for_each_hyper_col"][newRowNColNo["colNo"] || 0];
        const y = region_range["y_for_each_row"][newRowNColNo["rowNo"] || 0];
        document
          .querySelector("#main-container")
          .scrollTo(x - document.body.clientWidth / 2, y - 20);
      } else {
        const elevatorDom = document.querySelector(`#${regionName}`);
        document
          .querySelector("#main-container")
          .scrollTo(0, elevatorDom.offsetTop);
      }
    },
    changeRegionOffsetX(regionName, offsetX) {
      const regionOffsetX = { ...this.options.regionOffsetX };
      regionOffsetX[regionName] = offsetX;
      this.updateOptions({ regionOffsetX });
    },
    changeRegionHighlightNeuronRegExp(regionName, regExp) {
      const regionHighlightNeuronRegExp = {
        ...this.options.regionHighlightNeuronRegExp,
      };
      regionHighlightNeuronRegExp[regionName] = regExp;
      this.updateOptions({ regionHighlightNeuronRegExp });
    },
    highlightStaticPart(regionName, neuronNos) {
      const highlightStaticPart = { ...this.options.highlightStaticPart };
      highlightStaticPart[regionName] = neuronNos;
      this.updateOptions({ highlightStaticPart });
    },
    sendReadFileReq(stage = "") {
      setTimeout(() => {
        const { viewPortRange } = this;
        const data = {
          fileName: this.options.readFileName,
          viewPortRange,
          stage,
          options: this.options,
          urlParams,
        };
        this.sendMessage("readFile", data);
      }, 0);
    },
    updateOptions(opts, isSendReadFileReq = true) {
      this.options = { ...this.options, ...opts };
      setTimeout(this.setOptionStore, 0);
      if (isSendReadFileReq == true) {
        this.sendReadFileReq();
      } else if (isSendReadFileReq === false) {
        // do nothing
      } else {
        this.sendMessage(isSendReadFileReq, this.options);
      }
    },
    getOptionStore() {
      let optionStore = localStorage.getItem("OptionStore");
      const defaultOptions = {
        panelShow: true,
        showSomaProps: [],
        showNerveProps: [],
        showPinnedSomaNerveType: "out",
        isShowPinnedSomaCircuit: false,
        hideRestingNerve: false,
        onlyShowHistoryFileNames: [],
        elevatorAnchor: {},
        highlightStaticPart: {},
        regionOffsetX: {},
        regionHighlightNeuronRegExp: {},
        nowaFormProcess: "",
        hideRegions: [],
        layoutSize: "normal",
        readFileName: "",
        searchNerveExpressions: [
          { content: "", isCompressed: false, chartShowProps: [] },
        ],
        layoutContentSet: ["cortex"],
        searchNerveChartInd: -1,
        searchNerveEditorInd: -1,
      };
      return {
        ...defaultOptions,
        ...(optionStore ? JSON.parse(optionStore) : {}),
      };
    },
    setOptionStore() {
      localStorage.setItem("OptionStore", JSON.stringify(this.options));
    },
    onContextmenu(e) {
      e.preventDefault();
      this.showPanel(!this.options.panelShow);
    },
    showPanel(show = true) {
      this.updateOptions({ panelShow: show }, false);
    },
    sendMessage(type, data = {}) {
      console.log("[sendMessage]", type);
      ws.send(JSON.stringify({ type, data }));
    },
    listenScrollEnd(onScrollEnd) {
      let scrollTimer;
      const timeout = 200;
      document
        .querySelector("#main-container")
        .addEventListener("scroll", (e) => {
          clearTimeout(scrollTimer);
          scrollTimer = setTimeout(onScrollEnd, timeout);
        });
    },
    updateViewPortOnScrollEnd() {
      this.viewPortRange = this.getViewPortRange();
      this.sendReadFileReq("updateViewPortOnScrollEnd");
    },
    getViewPortRange() {
      const view = document.querySelector("#cortex");
      if (!view) {
        return { x0: 0, x1: 0, y0: 0, y1: 0, xCenter: 0, yCenter: 0 };
      }

      const viewRect = view.getBoundingClientRect();
      const [x0, x1] = [-viewRect.x, -viewRect.x + window.innerWidth];
      const [y0, y1] = [-viewRect.y, -(viewRect.y - window.innerHeight)];
      const [xCenter, yCenter] = [(x0 + x1) / 2, (y0 + y1) / 2];
      return { x0, x1, y0, y1, xCenter, yCenter };
    },
    addNewRegion() {
      this.sendMessage("add_region");
    },
    deleteRegion(regionInfo) {
      this.sendMessage("delete_region", {
        region_name: regionInfo.region_name,
      });
    },
    updateRegion(regionInfo) {
      return (updateContent) => {
        let newAllRegions = JSON.parse(JSON.stringify(this.fileData.region));
        const updateRegion = newAllRegions[regionInfo["region_no"]];
        _.merge(updateRegion.raw_region_json, updateContent);
        // this.fileData.region = newAllRegions;
        this.fileData = {
          ...fileData,
          region: newAllRegions,
        };
      };
    },
    saveRegion(regionInfo) {
      this.sendMessage("save_region", {
        region_info: regionInfo,
      });
    },
    addRegionNeuron(regionInfo, addAfterNeuronInfo) {
      this.sendMessage("add_neuron", {
        region_name: regionInfo.region_name,
        add_after_neuron_name: addAfterNeuronInfo.name,
      });
    },
    deleteRegionNeuron(regionInfo, deleteNeuronInfo) {
      this.sendMessage("delete_neuron", {
        region_name: regionInfo.region_name,
        delete_neuron_name: deleteNeuronInfo.name,
      });
    },
    addFormProcess() {
      this.sendMessage("add_form_process");
    },
    addConnect(fromData, toData, addWay = "add_connection") {
      if (!this.options.nowaFormProcess) {
        return;
      }
      this.sendMessage("add_connect", {
        form_process_name: this.options.nowaFormProcess,
        mother_data: fromData,
        father_data: toData,
        add_way: addWay,
      });
    },
    modifyConnect(connection) {
      this.sendMessage("modify_connect", {
        form_process_name: this.options.nowaFormProcess,
        connection,
      });
    },
    updateConnection(formProcess, connection) {
      return (updateContent) => {
        let newAllFormProcess = JSON.parse(
          JSON.stringify(this.fileData.allFormProcess)
        );
        const updateFormProcess = newAllFormProcess.find(
          (process) => process["process_name"] === formProcess["process_name"]
        );
        const updateConnection = updateFormProcess.connections.find(
          (c) => c["connection_name"] === connection["connection_name"]
        );
        _.merge(updateConnection, updateContent);
        this.fileData.allFormProcess = newAllFormProcess;
      };
    },
    requireSomaName(data) {
      const { region_no, neuron_no } = data;
      this.sendMessage("require_soma_name", { region_no, neuron_no });
    },
  },
};
</script>

<style>
#main-container {
  width: 100vw;
  height: 100vh;
  overflow: scroll;
}
</style>
