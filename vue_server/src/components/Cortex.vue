/* eslint-disable no-console */
<script>
import _ from "lodash";
import {
  Form,
  Select,
  Radio,
  Slider,
  Card,
  Collapse,
  Divider,
  Icon,
  List,
  Input,
  InputNumber,
  Button,
  Space,
  Switch,
  Tree,
  Tag,
  Tabs,
  Tooltip,
  Popconfirm,
  Layout,
  Checkbox,
  Menu,
} from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

const urlParams = new URLSearchParams(window.location.search);

export default {
  name: "Cortex",
  components: {},
  props: {
    appMode: { type: String, default: () => "" },
    marker: { type: Array, default: () => [] },
    regionRange: { type: Object, default: () => ({}) },
    cortexConsts: { type: Object, default: () => ({}) },
    nervePropsKeysMap: { type: Object, default: () => ({}) },
    somas: { type: Object, default: () => ({}) },
    somaPos: { type: Array, default: () => [] },
    nerves: { type: Object, default: () => ({}) },
    nervePos: { type: Object, default: () => ({}) },
    options: { type: Object, default: () => ({}) },
    updateOptions: { type: Function, default: () => { } },
    nerveType: { type: Object, default: () => ({}) },
    getViewPortRange: { type: Function, default: () => { } },
    addConnect: { type: Function, default: () => { } },
    allFormProcess: { type: Array, default: () => [] },
    hoverSomaName: { type: String, default: () => "" },
    requireSomaName: { type: Function, default: () => { } },
  },
  computed: {
    cortexRange() {
      const regionRangeList = Object.values(this.regionRange);
      let [w, h] = [0, 0];
      regionRangeList.forEach((r) => {
        w = Math.max(w, r.x_end);
        h = Math.max(h, r.y_end);
      });
      return [w, h];
    },
    allConnections() {
      let allConnections = [];
      this.allFormProcess.map((formProcess) => {
        allConnections = allConnections.concat(formProcess.connections);
      });
      return allConnections;
    },
  },
  render() {
    const [cortexW, cortexH] = this.cortexRange;
    const canRender = this.options.layoutContentSet.slice(-1)[0] === 'cortex';
    return (
      <div
        id="cortex"
        class="cortex"
        ref="cortex"
        style={{
          width: `${cortexW}px`,
          height: `${cortexH}px`,
        }}
      >
        {canRender && this.renderSomas()}
        {canRender && this.renderNerves()}
        {canRender && this.renderRegionInfos()}
        {canRender && this.options.layoutSize !== 'extreme_small' && this.renderHyperColInfos()}
      </div>
    );
  },
  data() {
    return {
      tooltip: {},
      editModeNewConnectFrom: {},
    };
  },
  mounted() { },
  methods: {
    getPartProp(partDataList, propName) {
      return partDataList[propName];
    },
    renderSomas() {
      const { somaPos } = this;
      return (this.somas["type"] || []).map((_, ind) => {
        const [x, y] = somaPos[ind];
        const pos = { x, y };
        const data = Object.fromEntries(
          Object.keys(this.somas).map((key) => [key, this.somas[key][ind]])
        );
        return this.somaTemp(data, pos);
      });
    },
    renderNerves() {
      const { nervePos, nerves } = this;
      return (nerves["type"] || []).map((_, ind) => {
        const { from_x, from_y, to_x, to_y, x, y } = Object.fromEntries(
          Object.keys(nervePos).map((key) => [key, nervePos[key][ind]])
        );
        const pos = { x, y };
        const fromPos = { x: from_x, y: from_y };
        const toPos = { x: to_x, y: to_y };
        const nerve = Object.fromEntries(
          Object.keys(nerves).map((key) => [key, nerves[key][ind]])
        );
        const nerveColor = this.getNerveColor(nerve);
        return this.nerveTemp(nerve, pos, fromPos, toPos, nerveColor);
      });
    },
    renderRegionInfos() {
      return Object.keys(this.regionRange || {}).map((regionName) => {
        const regionRange = this.regionRange[regionName];
        return (
          <div
            id={regionName}
            class="region-info"
            style={{
              top: `${regionRange.y_start - 22}px`,
              left: `${regionRange.x_start}px`,
            }}
          >
            {regionName}
          </div>
        );
      });
    },
    renderHyperColInfos() {
      return Object.values(window.region || {})
        .filter(
          (regionInfo) => Object.keys(regionInfo.neurons || {}).length > 0
        )
        .map((regionInfo) => {
          const regionName = regionInfo["region_name"];
          const regionRange = this.regionRange[regionName];
          const { region_shape } = regionInfo;
          const [rowSum, hyperColSum] = region_shape;
          const { x_for_each_hyper_col, y_for_each_row } = regionRange;
          return _.range(rowSum).map((rowNo) => {
            return _.range(hyperColSum).map((colNo) => {
              const pos = `${rowNo}:${colNo}`;
              const infoTop = y_for_each_row[rowNo];
              const infoLeft = x_for_each_hyper_col[colNo] - 30;
              return (
                <div
                  key={`${regionName}:${pos}`}
                  class="hyper-col-pos"
                  style={{
                    top: `${infoTop}px`,
                    left: `${infoLeft}px`,
                  }}
                >
                  <div>{`${pos}`}</div>
                </div>
              );
            });
          });
        });
    },
    somaTemp(data, pos) {
      const { getPartProp, options } = this;
      const { region } = window;
      const { cycle_r, active_potential, dendrite_type, type } =
        this.cortexConsts;
      const size = cycle_r * 2 + 1;
      const thisSomaIsActuallyADendrite = Object.values(dendrite_type).includes(
        getPartProp(data, "type")
      );
      const thisSomaIsActuallyAnAxon =
        getPartProp(data, "type") == type["axon"];
      const backgroundColor =
        parseInt(getPartProp(data, "excite")) >= active_potential
          ? "tomato"
          : "#61afef";
      const somaInlineStyle = `
        width: ${size}px; 
        height: ${size}px;
        background-color:${backgroundColor};
        border-radius:${size}px
      `;
      const dendriteInlineStyle = `
        width: 0;
        height: 0;
        border: ${size / 2}px solid transparent;
        border-bottom: ${size}px solid ${backgroundColor};
        transform: translateY(-50%);
      `;
      const axonInlineStyle = `
        width: ${size}px; 
        height: ${size}px;
        background-color:${backgroundColor};
      `;
      const { neuronInfo = {} } =
        this.getRegionAndNeuronInfoWithNeuronData(data);
      return (
        <div
          key={getPartProp(data, "ind")}
          class={`soma`}
          style={`
            left:${pos.x}px;
            top:${pos.y}px;${thisSomaIsActuallyADendrite
              ? dendriteInlineStyle
              : thisSomaIsActuallyAnAxon
                ? axonInlineStyle
                : somaInlineStyle
            }`}
          onClick={() => this.onSomaClick(data)}
          onMousedown={() => this.onSomaMouseDown(data)}
          onMouseup={() => this.onSomaMouseUp(data)}
        >
          <div
            class="soma-info"
          >
            {this.getInfoStr(data, this.options.showSomaProps || [])}
          </div>
          {
            <div class="soma-name">{neuronInfo.name}</div>
          }
        </div>
      );
    },
    nerveTemp(data, pos, fromPos, toPos) {
      const { getPartProp } = this;
      const { nerve_w, active_potential } = this.cortexConsts;
      const rotate = this.getRotate(fromPos, toPos);
      const [length] = this.getDistance(fromPos, toPos);
      const color = this.getNerveColor(data);
      const isExcite =
        parseInt(getPartProp(data, "excite")) >= active_potential;
      const infoStr = this.getInfoStr(data, this.options.showNerveProps || []);
      const LTPOpacityRatio =
        parseFloat(getPartProp(data, "LTP")) /
        parseFloat(urlParams.get("maxLTP"));
      const isVisibility =
        urlParams.get("minExcite") &&
        parseFloat(getPartProp(data, "excite")) >=
        parseFloat(urlParams.get("minExcite"));
      const FaOpacityRatio =
        parseFloat(getPartProp(data, "Fa")) /
        parseFloat(urlParams.get("maxFa"));

      return (
        <div
          class="nerve"
          style={{
            left: fromPos.x + "px",
            top: fromPos.y + "px",
            width: length + "px",
            height: nerve_w + "px",
            transform: `rotate(${rotate}deg)`,
            backgroundColor: color,
            // visibility: isVisibility ? "visible" : "hidden",
            opacity: LTPOpacityRatio || FaOpacityRatio,
            border: `${isExcite ? 1 : 0}px solid #f44336`,
          }}
          onClick={() => this.onNerveClick(data, pos, fromPos, toPos)}
          oncontextmenu={(e) => this.onNerveContextmenu(e, data)}
          onMouseover={(e) => this.onNeveMouseover(data, infoStr, e)}
          onMouseleave={() => this.onNerveMouseleave()}
          onMouseup={() => this.onNerveMouseUp(data)}
        >
          <div
            class="nerve-info"
            style={{
              transform: `translateX(50%) translateY(-50%) rotate(${-rotate}deg)`,
              color,
              // right: '90%',
              right: "80%",
              // right: '30%',
            }}
          >
            {infoStr}
          </div>
        </div>
      );
    },
    getRotate(pos1, pos2) {
      return Math.atan2(pos2.y - pos1.y, pos2.x - pos1.x) / (Math.PI / 180);
    },
    getDistance(pos1, pos2) {
      const dx = pos2.x - pos1.x;
      const dy = pos2.y - pos1.y;
      const dz = Math.sqrt(dx * dx + dy * dy);
      return [dz, dx, dy];
    },
    getRegionAndNeuronInfoWithNeuronData(neuronData) {
      // return { regionInfo: {}, neuronInfo: {} };

      const { getPartProp } = this;
      const regionInfo = window.region[getPartProp(neuronData, "region_no")];
      const neuronInfo = Object.values(regionInfo["neurons"]).find(
        (r) => r.neuron_no === getPartProp(neuronData, "neuron_no")
      );
      return { regionInfo, neuronInfo };
    },
    getNerveLineOffset(nerve, nerveList, parentPos1, parentPos2) {
      const allMarkerExinfoSorted = this.nerves
        .map((n) => n["marker_exinfo"])
        .sort();
      const thisNerveLineOrderNo = allMarkerExinfoSorted.findIndex(
        (exinfo) => nerve["marker_exinfo"] === exinfo
      );
      const unit_offset = 3;
      const lineOffset = thisNerveLineOrderNo * unit_offset;
      const rotate = this.getRotate(parentPos1, parentPos2);
      const linePointOffset = {
        x: -Math.sin((2 * Math.PI) / rotate) * lineOffset,
        y: Math.cos((2 * Math.PI) / rotate) * lineOffset,
      };
      return linePointOffset;
    },
    getNerveColor(data) {
      const { nerveType, getPartProp } = this;
      return {
        [`${nerveType.axon}`]: "red", // axon
        [`${nerveType.axonEnd}`]: "orange", // axon end
        [`${nerveType.dendrite}`]: "blue", // dendrite
        [`${nerveType.dendrite_nor}`]: "green", // dendrite
      }[getPartProp(data, "type")];
    },
    getInfoStr(data, keys) {
      const { getPartProp } = this;
      const PROPVAL_TOFIXED_LENGTH = 1;
      return keys
        .map((key) => {
          let propVal = getPartProp(data, key);
          if (!isNaN(+propVal)) {
            propVal = +propVal;
            if ((String(propVal).split('.')[1] || '').length > PROPVAL_TOFIXED_LENGTH) {
              propVal = propVal.toFixed(PROPVAL_TOFIXED_LENGTH);
            }
            if (
              key === "excite" &&
              Math.abs(propVal) >= 10000 &&
              Math.abs(propVal) < 10000 * 10000
            ) {
              // propVal = `${(propVal / 10000).toFixed(1)}w`;
            } else if (
              key === "excite" &&
              Math.abs(propVal) >= 10000 * 10000 &&
              Math.abs(propVal) < 10000 * 10000 * 10000
            ) {
              propVal = `${(propVal / (10000 * 10000)).toFixed(1)}ww`;
            } else if (
              key === "excite" &&
              Math.abs(propVal) >= 10000 * 10000 * 10000
            ) {
              propVal = `${(propVal / (10000 * 10000 * 10000)).toFixed(1)}www`;
            }
          }
          let infoStr = `${propVal !== undefined ? propVal : ""}`;
          return infoStr;
        })
        .join(" ");
    },
    onSomaClick(data) {
      this.updatepinnedSomaInds(data);
    },
    // onSomaContextmenu(event, data) {
    //   event.preventDefault();
    //   event.stopPropagation();
    //   this.updatePinnedCls(data);
    // },
    onSomaMouseDown(data) {
      // if (this.appMode === "edit") {
      this.editModeRecordNewConnectFrom(data);
      // }
    },
    onSomaMouseUp(data) {
      const { regionInfo, neuronInfo } =
        this.getRegionAndNeuronInfoWithNeuronData(data);
      const editModeNewConnectTo = {
        ...neuronInfo,
        region_name: regionInfo.region_name,
        data,
      };
      const ADD_WAY =
        this.appMode === "edit" ? "add_connection" : "copy_connection";
      const { getPartProp } = this;
      if (
        getPartProp(this.editModeNewConnectFrom.data, "ind") !==
        getPartProp(editModeNewConnectTo.data, "ind")
      ) {
        this.addConnect(
          this.editModeNewConnectFrom,
          editModeNewConnectTo,
          ADD_WAY
        );
      }
    },
    onSomaMouseOver(data) {
      this.requireSomaName(data);
    },
    onNerveClick(data, pos, fromPos, toPos) {
      this.anchor2NerveFarawayParentPos(fromPos, toPos);
    },
    onNerveContextmenu(e, data) {
      e.preventDefault();
      e.stopPropagation();
      this.updatepinnedNerveInds(data);
    },
    onNeveMouseover(data, infoStr, e) {
      const nerveInfo = this.exchangePartDataToMap(data);
      // console.log("[onNeveMouseover]", nerveInfo);
      this.options.showNerveProps.map((key) => {
        console.log(key, data[key], "\n");
      });
      this.setToolTip("show", infoStr, {
        x: e.pageX,
        y: e.pageY,
      });
    },
    onNerveMouseleave() {
      this.setToolTip("hide");
    },
    onNerveMouseUp(data) {
      const { getPartProp } = this;
      console.log(this.allConnections);
      const motherMarker = getPartProp(data, "mother_marker");
      const fatherMarker = getPartProp(data, "father_marker");
      const connection = this.allConnections.find((connection) => {
        return (
          connection.mother_info["marker"] == motherMarker &&
          connection.father_info["marker"] == fatherMarker
        );
      });
      if (
        getPartProp(this.editModeNewConnectFrom.data, "ind") !==
        getPartProp(data, "ind")
      ) {
        this.addConnect(this.editModeNewConnectFrom, {
          ...connection,
          data,
        });
      }
    },
    editModeRecordNewConnectFrom(somaData) {
      const { regionInfo, neuronInfo } =
        this.getRegionAndNeuronInfoWithNeuronData(somaData);
      this.editModeNewConnectFrom = {
        ...neuronInfo,
        region_name: regionInfo.region_name,
        data: somaData,
      };
    },
    setToolTip(showOrHide, cont, pos) {
      this.tooltip = {
        showOrHide,
        cont,
        pos,
      };
    },
    updatepinnedSomaInds(data) {
      const { getPartProp } = this;
      const item = getPartProp(data, "ind");
      const newPinnedIds = new Set([...(this.options.pinnedSomaInds || [])]);
      newPinnedIds.has(item)
        ? newPinnedIds.delete(item)
        : newPinnedIds.add(item);
      this.updateOptions({
        pinnedSomaInds: [...newPinnedIds],
      });
    },
    updatepinnedNerveInds(data) {
      const { getPartProp } = this;
      const item = getPartProp(data, "ind");
      const newPinnedIds = new Set([...(this.options.pinnedNerveInds || [])]);
      newPinnedIds.has(item)
        ? newPinnedIds.delete(item)
        : newPinnedIds.add(item);
      this.updateOptions({
        pinnedNerveInds: [...newPinnedIds],
      });
    },
    consolePartInfo(data) {
      console.info(`%c ${JSON.stringify(data)}`, "color:blue;");
    },
    anchor2NerveFarawayParentPos(fromPos, toPos) {
      const { xCenter, yCenter } = this.getViewPortRange();
      const fromPosDistance = this.getDistance(fromPos, {
        x: xCenter,
        y: yCenter,
      })[0];
      const toPosDistance = this.getDistance(toPos, {
        x: xCenter,
        y: yCenter,
      })[0];
      const farawayPos = fromPosDistance > toPosDistance ? fromPos : toPos;
      document.querySelector('#main-container').scrollTo(
        farawayPos.x - document.body.clientWidth / 2,
        farawayPos.y - document.body.clientHeight / 2
      );
    },
    exchangePartDataToMap(partData) {
      const partInfoMap = {};
      Object.keys(this.nervePropsKeysMap).map((propName) => {
        partInfoMap[propName] = this.getPartProp(partData, propName);
      });
      return partInfoMap;
    },
  },
};
</script>

<style lang="less">
// @import '~ant-design-vue/dist/antd.dark.less';

body {
  background-color: rgb(40, 44, 52);
  color: #abb2bf;
}

.cortex {
  position: relative;
  // margin: 20px 20px 100px 120px;
  margin-bottom: 100px;
}

.soma {
  position: absolute;
  width: 8px;
  height: 8px;
  line-height: 12px;
  font-size: 12px;
  // color: black;
  z-index: 2;

  // &.highlight {
  //   transform: scale(1.15);
  //   box-shadow: -2px 2px 3px rgba(0, 0, 0, 0.75);
  // }
  .soma-info {
    z-index: 5;
    position: absolute;
    top: 7px;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
    // width: 100px;
    text-align: center;
    user-select: none;
  }

  &:hover {
    z-index: 3;

    .soma-name {
      visibility: visible;
      // width: 200px;
    }

    .soma-info {
      background-color: #fff;
      border: 1px solid #999;
    }
  }

  .soma-name {
    position: absolute;
    // top: -14px;
    top: 0px;
    left: 50%;
    transform: translateX(-50%) translateY(-100%);
    visibility: hidden;
    // background-color: #fff;
    // pointer-events: none;
    text-overflow: ellipsis;
    z-index: 5;
    // width: 150px;
    width: 200px;
    overflow: hidden;
    text-align: center;
    background-color: #fff;
    border: 1px solid #999;
  }
}

.nerve {
  position: absolute;
  height: 5px;
  transform-origin: 0 center;
  opacity: 0.5;
  z-index: 1;
  box-sizing: content-box;

  &:hover {
    opacity: 1 !important;
    z-index: 10;

    .nerve-info {
      background-color: #fff;
    }
  }

  &::before {
    content: " ";
    margin-right: 10px;
    float: right;
    display: block;
    width: 1px;
    height: 1px;
    background-color: black;
  }

  .nerve-info {
    transform-origin: center center;
    position: absolute;
    right: 50%;
    // pointer-events: none;
    // top: 50%;
  }

  .nerve-end {
    position: absolute;
    background-color: black;
    right: 0;
    top: -1px;
  }
}

.region-info {
  position: absolute;
  // user-select: none;
}

.hyper-col-pos {
  position: absolute;
  text-align: center;
  transform: translateY(-15px);
  user-select: none;
}
</style>