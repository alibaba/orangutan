<script>
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
} from "ant-design-vue";
import "ant-design-vue/dist/antd.css";
import MonacoEditor from "vue-monaco";
import grayMatrixList from "../data/orient_receptive.json";
import html2canvas from "html2canvas";
import JSZip from "jszip";
const LAYOUT_CONTENT_NAMES = {
  cortex: "cortex",
  circuitTreePanel: "circuitTreePanel",
  searchNerveEditor: "searchNerveEditor",
  searchNerveChart: "searchNerveChart",
  circuitTreeChart: "circuitTreeChart",
};
import saccadeDataList0229 from "../data/saccadeDataList/0229.json";
import saccadeDataList0310 from "../data/saccadeDataList/0310.json";
import saccadeDataList0311 from "../data/saccadeDataList/0311.json";
import saccadeDataList0313 from "../data/saccadeDataList/0313.json";
import saccadeDataList0314 from "../data/saccadeDataList/0314.json";
import saccadeDataList0315 from "../data/saccadeDataList/0315.json";
import saccadeDataList0317 from "../data/saccadeDataList/0317.json";
import saccadeDataList0318 from "../data/saccadeDataList/0318.json";
import saccadeDataList0319 from "../data/saccadeDataList/0319.json";
import saccadeDataList0320 from "../data/saccadeDataList/0320.json";
import saccadeDataList0320_1 from "../data/saccadeDataList/0320_1.json";
import saccadeDataList0321 from "../data/saccadeDataList/0321.json";
import saccadeDataList0324 from "../data/saccadeDataList/0324.json";
import saccadeDataList0325 from "../data/saccadeDataList/0325.json";
import saccadeDataList0326 from "../data/saccadeDataList/0326.json";
import saccadeDataList0327 from "../data/saccadeDataList/0327.json";
import saccadeDataList0327ForPaper from "../data/saccadeDataList/0327_for_paper.json";

function mixupSaccadeDataList(lists) {
  if (lists.length === 0) return lists;
  return lists[0]
    .map((_, ind) => {
      return lists.map((li) => li[ind]);
    })
    .flat();
}

export default {
  name: "Panel",
  props: {
    appMode: { type: String, default: () => "" },
    visible: { type: Boolean, default: false },
    somas: { type: Object, default: () => ({}) },
    nerves: { type: Object, default: () => ({}) },
    options: { type: Object, default: () => ({}) },
    updateOptions: { type: Function, default: () => {} },
    allFileName: { type: Array, default: () => [] },
    showPanel: { type: Function, default: () => {} },
    nervePropsKeysMap: { type: Object, default: () => ({}) },
    setReadFileName: { type: Function, default: () => {} },
    gotoElevator: { type: Function, default: () => {} },
    highlightStaticPart: { type: Function, default: () => {} },
    TYPE: { type: Object, default: () => ({}) },
    addNewRegion: { type: Function, default: () => {} },
    deleteRegion: { type: Function, default: () => {} },
    addRegionNeuron: { type: Function, default: () => {} },
    deleteRegionNeuron: { type: Function, default: () => {} },
    addFormProcess: { type: Function, default: () => {} },
    allFormProcess: { type: Array, default: () => [] },
    getPartProp: { type: Function, default: () => {} },
    updateConnection: { type: Function, default: () => {} },
    updateRegion: { type: Function, default: () => {} },
    saveRegion: { type: Function, default: () => {} },
    modifyConnect: { type: Function, default: () => {} },
    cortexConsts: { type: Object, default: () => ({}) },
    allGrayMaskPath: { type: Array, default: () => [] },
    changeRegionOffsetX: { type: Function, default: () => {} },
    changeRegionHighlightNeuronRegExp: { type: Function, default: () => {} },
    searchNerveResult: { type: Array, default: () => [] },
  },
  data() {
    return {
      configKonva: {
        width: 200,
        height: 200,
      },
      configCircle: {
        x: 100,
        y: 100,
        radius: 70,
        fill: "red",
        stroke: "black",
        strokeWidth: 4,
      },
      showTimelineTooltips: undefined,
      hoverChartBarData: {},
      showChartTooltip: false,
      canRenderLayoutContent: true,
      grayMatrixInd: 0,
      // saccadeDataList,
      saccadeDataList: mixupSaccadeDataList([
        // 问题：注意到角点处尺度为1的内轮廓中心
        // 案例：'1_2','1_6','3_1','3_6','4_1','4_2','4_3','4_8','6_4','6_9','7_4','7_8','8_1','8_9','9_2','9_3','9_6','9_9',
        // 原因：角点处存在大量尺度为1的内轮廓直线，对尺度为1的内轮廓中心形成较大激励
        // 思路：区分角点处的内轮廓中心和非角点处的轮廓中心，角点处存在射线，非角点处不存在射线
        // 解法：用角点处的射线来抑制角点处的内轮廓中心
        // saccadeDataList0311,
        // 问题：为了解决角点问题，导致部分尺度较小（s3~s7）的内轮廓中心没有被注意到
        // 案例：'2_5','3_8','6_6','6_7','6_9','8_0','8_1','8_2','8_5','8_7','9_0','9_7','9_8',
        // 原因：尺度较小的内轮廓中心附近处容易存在边缘点，导致该位置上的射线细胞被这些边缘点激活，进而抑制内轮廓中心
        // 思路：区分角点处的内轮廓中心和非角点处的轮廓中心，角点处存在射线，非角点处不存在射线
        // 解法：用更大尺度的内轮廓方位来抑制这些射线
        // saccadeDataList0313,
        // 问题：在尝试用更大尺度的内轮廓方位来抑制位于内轮廓的射线后，发现部分射线无法被有效抑制，导致注意到特征角
        // 案例：'2_5','8_1'
        // 原因：
        //   1. 射线的起点位于某个像素点上，后者产生了一个边缘点，进而在该处激活了尺度为1的外轮廓方位，抑制住了该位置上的内轮廓方位，导致无法有效抑制射线（2_5）
        //   2. 向内的轻微曲线会导致射线末端的垂直方位和内轮廓方位都不显著，对射线的抑制作用较小（8_1）
        // 解法：用末端上的像素点来抑制射线，作为对末端上的内轮廓方位和垂直方位的补充
        // saccadeDataList0314,
        // 问题：部分case下的角没有注意到
        // 案例：'3_3','8_9', | '5_9',
        // 原因：用末端上的像素点来抑制射线，可能会将正常的微曲射线也抑制住
        // 思路：还是需要用内轮廓方位来抑制，但是单个边缘点的兴奋可能不够大，导致用于抑制射线的内轮廓方位作用有限
        // 解法：改用求和方位来抑制射线
        // saccadeDataList0315,
        // 问题：又发现部分case中存在注意到内轮廓中的角的问题
        // 案例：'2_3','2_5','4_4','6_9','7_7','9_7',
        // saccadeDataList0317,
        // 问题：9_6没有注意到左下的角
        // 案例：'9_6','8_9','7_9','4_5',
        // 原因：9_6，因为COri^{o=270,s=1}兴奋过小，导致CRay^{o=270,s=5}被拮抗回路过度抑制，进而导致CAng^{o1=180,o2=270}兴奋过小
        // 解法：
        //  1. 9_6，适当减少拮抗回路的抑制作用
        //  2. 增加尺度对于角的增益
        // saccadeDataList0318,
        // 问题：关注到不符合预期的角
        // 案例：'9_0','4_7','3_7','3_4','3_6','2_4',
        // 原因：过度增益了尺度
        // 解法：适当降低尺度增益
        // saccadeDataList0319,
        // 7_7里那么大尺度的一个角居然没被注意到
        // 原因：之前禁止了对21尺度的射线的感知，导致这个角直接被干掉了。。。
        // 解法：尝试解禁21

        // 问题：一些开口的小尺度内轮廓还是会被射线抑制，因为在开口处不存在内轮廓中心，无法有效抑制射线
        // 案例：'4_5','3_7','3_4','3_3','2_4','2_2','2_0',
        // 解法：改成让射线只针对尺度为1的内轮廓方位进行抑制
        // saccadeDataList0320,
        // saccadeDataList0320_1,
        // 基本上只剩下了一些小问题或可以被解释的问题
        // 9_9 9_6 6_9 4_5 3_4 2_5
        // saccadeDataList0321,
        // saccadeDataList0324,
        // 问题：发现大量注意到感受野存在交集的特征
        // 案例：'7_8','7_3','7_2','7_1','7_0','6_8','5_7','4_5','2_4','2_3','2_0','1_9','1_8','1_7','1_6','1_3','1_1','1_0','0_9','0_2',
        // 原因：看下来基本都是内轮廓的反馈问题
        // saccadeDataList0325,
        // saccadeDataList0326,
        // saccadeDataList0327,
        saccadeDataList0327ForPaper,
      ]),
      saccadeDataMap: {},
      backPropagationBase64Map: [],
    };
  },
  computed: {
    saccadePathList() {
      function extractXY(str = "") {
        // 正则表达式用于匹配 y= 和 x= 后面的数字
        const regex = /y=(\d+),x=(\d+)/;
        // 使用正则表达式提取匹配的值
        const match = str.match(regex);

        if (match) {
          // match[1] 是第一个捕获组 (y对应的数字)，match[2] 是第二个捕获组 (x对应的数字)
          return {
            y: parseInt(match[1], 10),
            x: parseInt(match[2], 10),
          };
        }

        // 如果没有匹配到，返回null或者其他表示错误的值
        return null;
      }

      const squareColors = ["D80073", "1BA1E2", "60A917", "E3C800", "A0522D"];
      const dataList = this.saccadeDataList
        .filter(([mnist, _]) => {
          // return true
          return [
            "0_0",
            "0_1",
            "1_0",
            "1_1",
            "2_0",
            "2_1",
            "3_0",
            "3_1",
            "4_0",
            "4_1",
            "5_0",
            "5_1",
            "6_0",
            "6_1",
            "7_0",
            "7_1",
            "8_0",
            "8_1",
            "9_0",
            "9_1",
          ].includes(mnist);
        })
        .map(([mnist, latexList]) => {
          return [
            mnist,
            latexList.map((latex) => Object.values(extractXY(latex))),
            latexList.map((latex) => latex.split("_")[0]),
          ];
        });
      return dataList.map(([mnist, posList, featureList]) => {
        const pathList = posList
          .map((pos, posInd) => {
            const color = squareColors[posInd];
            const x = (pos[1] - 1) * 10;
            const y = (pos[0] - 1) * 10;
            const pos1 = posList[posInd + 1] || [];
            const x1 = (pos1[1] - 1) * 10;
            const y1 = (pos1[0] - 1) * 10;
            const distance = Math.sqrt(
              Math.pow(x - x1, 2) + Math.pow(y - y1, 2)
            );
            const arrowOffsetRatio = 1 - 10 / distance;
            return [
              {
                Ang: {
                  type: "rect",
                  config: {
                    x,
                    y,
                    width: 10,
                    height: 10,
                    fill: "#" + color,
                  },
                },
                Arc: {
                  type: "circle",
                  config: {
                    x: x + 5,
                    y: y + 5,
                    radius: 5,
                    fill: "#" + color,
                  },
                },
              }[featureList[posInd]],
              // 箭头
              ...(posInd === posList.length - 1
                ? []
                : [
                    {
                      type: "arrow",
                      config: {
                        points: [
                          x + 5,
                          y + 5,
                          x + (x1 - x) * arrowOffsetRatio + 5,
                          y + (y1 - y) * arrowOffsetRatio + 5,
                        ],
                        stroke: "#" + color,
                        strokeWidth: 3,
                        fill: "#" + color,
                        zIndex: 100,
                        pointerWidth: 5,
                        pointerLength: 5,
                      },
                    },
                  ]),
            ];
          })
          .flat()
          .reverse();
        return [mnist, pathList];
      });
    },
    allProps() {
      return Object.keys(this.nervePropsKeysMap);
    },
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
    somasMap() {
      const map = {};
      const { somas } = this;
      (somas["ind"] || []).map((id, ind) => {
        map[id] = Object.fromEntries(
          Object.keys(somas).map((key) => [key, somas[key][ind]])
        );
      });
      return map;
    },
    nervesMap() {
      const map = {};
      const { nerves } = this;
      (nerves["ind"] || []).map((id, ind) => {
        map[id] = Object.fromEntries(
          Object.keys(nerves).map((key) => [key, nerves[key][ind]])
        );
      });
      return map;
    },
    allNerveMap() {
      return {
        ...this.nervesMap,
        ...this.somasMap,
      };
    },
    readFileName() {
      return this.options.readFileName;
    },
  },
  watch: {
    somas(newVal, oldVal) {
      const [tickName, writeStageName, mnist] =
        this.options.readFileName.split(";");
      if (writeStageName === "back_propagation_to_dot") {
        const imageMargin = 20;
        const imageSize = 280;
        setTimeout(() => {
          html2canvas(document.querySelector("#matrixList"), {
            x: imageMargin,
            // y: imageMargin,
            width: imageSize,
            height: imageSize,
            scale: 0.25,
          }).then((canvas) => {
            var dataURL = canvas.toDataURL("image/png");
            this.backPropagationBase64Map[mnist] =
              this.backPropagationBase64Map[mnist] || [];
            this.backPropagationBase64Map[mnist].push(dataURL);
            // console.log(
            //   "[backPropagationBase64Map]",
            //   mnist,
            //   this.backPropagationBase64Map[mnist]
            // );
          });
        }, 100);
      }
    },
  },
  created() {},
  mounted() {
    this.redrawLayoutContent();
  },
  render(h) {
    return (
      <Layout class="panel-layout" id="panel-layout">
        <Layout
          style={{
            background: "transparent",
          }}
        >
          <Layout.Sider
            theme="light"
            width="300px"
            collapsed={!this.options.showSider}
            collapsedWidth="0"
            style={{
              padding: "10px",
              boxShadow: "rgb(1 1 1 / 30%) 0px 0px 10px",
              zIndex: 1,
              pointerEvents: "all",
            }}
          >
            {this.renderElevatorPanel()}
          </Layout.Sider>
          <Layout.Content class="panel-layout-content">
            {this.canRenderLayoutContent &&
              (
                {
                  [LAYOUT_CONTENT_NAMES.cortex]: new Function(),
                  [LAYOUT_CONTENT_NAMES.circuitTreePanel]:
                    this.renderCircuitTreePanel,
                  [LAYOUT_CONTENT_NAMES.circuitTreeChart]:
                    this.renderCircuitTreeChart,
                  [LAYOUT_CONTENT_NAMES.searchNerveChart]:
                    this.renderSearchNerveChart,
                  [LAYOUT_CONTENT_NAMES.searchNerveEditor]:
                    this.renderSearchNerveEditor,
                }[(this.options.layoutContentSet || []).slice(-1)[0]] ||
                new Function()
              )()}

            {/* 图表tooltip */}
            {this.renderChartTooltip()}

            {this.renderSaccadePathway()}

            {/* 灰度图预览 */}
            {this.renderGrayMatrixPreviewWithMapData()}
            {/* {this.renderGrayMatrixPreviewWithListData()} */}
            {/* {this.renderMultiFieldGrayMatrixPreviewWithMapData()} */}
          </Layout.Content>
          <Layout.Sider
            theme="light"
            width="300px"
            collapsed={!this.options.showSider}
            collapsedWidth="0"
            style={{
              padding: "10px",
              boxShadow: "rgb(1 1 1 / 30%) 0px 0px 10px",
              overflow: "scroll",
              zIndex: 1,
              pointerEvents: "all",
            }}
          >
            {this.renderFilterPanel()}
          </Layout.Sider>
        </Layout>
        <Layout.Footer
          style={{
            padding: 0,
            zIndex: 1,
            pointerEvents: "all",
            display: "flex",
            flexDirection: "row",
            background: "#fff",
            overflow: "hidden",
            borderTop: "1px solid #ccc",
          }}
        >
          <Icon
            type="layout"
            style={{
              padding: "13px",
            }}
            onClick={() => {
              this.updateOptions(
                {
                  showSider: !this.options.showSider,
                },
                false
              );
              // 布局改变时需要触发图表重绘
              setTimeout(this.redrawLayoutContent, 200);
            }}
          />
          {this.renderTimelineSlider()}
        </Layout.Footer>
      </Layout>
    );
  },
  methods: {
    zipDownloadBase64(base64List, nameList = [], folderName = "canvas-images") {
      console.log("[zipDownloadBase64]");

      var zip = new JSZip();

      base64List.forEach((base64, ind) => {
        zip.file(
          (nameList[ind] || `canvas${ind}`) + ".png",
          base64.replace("data:image/png;base64,", ""),
          { base64: true }
        );
      });

      // 生成ZIP文件并触发下载
      zip.generateAsync({ type: "blob" }).then(function (content) {
        // 创建一个临时链接元素
        var link = document.createElement("a");

        // 使用window.URL.createObjectURL()创建blob的URL
        link.href = window.URL.createObjectURL(content);

        // 设置下载属性及文件名
        link.download = `${folderName}.zip`;

        // 触发下载动作
        link.click();
      });
    },
    recordSaccadeNode(mnist, node) {
      this.saccadeDataMap[mnist] = this.saccadeDataMap[mnist] || [];
      if (window.lastNode === node) return;
      window.lastNode = node;

      this.saccadeDataMap[mnist].push(node);
      this.saccadeDataList = Object.entries(this.saccadeDataMap);
      localStorage.setItem(
        "saccadeDataList",
        JSON.stringify(this.saccadeDataList)
      );
      // console.log("[recordSaccadeNode]", mnist, node, this.saccadeDataList);
    },
    renderGrayMatrixPreviewWithMapData() {
      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            overflow: "scroll",
          }}
        >
          <div
            id="receptiveFieldMatrix"
            style={{
              width: "fit-content",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "row",
                marginLeft: "100px",
              }}
            >
              {/* {Array(8)
                .fill("")
                .map((_, ind) => (
                  <div
                    style={{
                      minWidth: "100px",
                      margin: "0 10px",
                      display: "flex",
                      flexDirection: "row",
                      justifyContent: "center",
                    }}
                  >
                    orient: {(ind + 1 + 8) * 22.5}
                  </div>
                ))} */}
            </div>
            {Object.entries(grayMatrixList).map(
              ([fieldLevel, grayMatrixItem]) => {
                return (
                  <div style={{ display: "flex", flexDirection: "row" }}>
                    {/* <div
                      style={{
                        minWidth: "100px",
                        height: "100px",
                        lineHeight: "100px",
                        textAlign: "right",
                        margin: "10px 0",
                      }}
                    >
                      scale: {Math.floor(fieldLevel / 2) + 1}
                    </div> */}
                    {Object.entries(grayMatrixItem).map(([orient, data]) => {
                      return (
                        <div
                          style={{
                            minWidth: "100px",
                            height: "100px",
                            margin: "10px",
                            background: "#fff",
                            display: "flex",
                            flexDirection: "column",
                            justifyContent: "space-between",
                          }}
                        >
                          {data.map((row, rowInd) => (
                            <div
                              style={{
                                width: "100%",
                                height: `${100 / data.length}%`,
                                display: "flex",
                              }}
                            >
                              {row.map((x, colInd) => (
                                <div
                                  style={{
                                    height: "100%",
                                    width: `${100 / row.length}%`,
                                    background:
                                      rowInd === Math.floor(data.length / 2) &&
                                      colInd === Math.floor(data.length / 2)
                                        ? "#1BA1E2"
                                        : `rgba(0,0,0,${x / 255})`,
                                    border: "0.5px solid black",
                                  }}
                                ></div>
                              ))}
                            </div>
                          ))}
                        </div>
                      );
                    })}
                  </div>
                );
              }
            )}
          </div>

          <Button
            type={"primary"}
            style={{ width: "100%" }}
            onClick={() => {
              html2canvas(
                document.querySelector("#receptiveFieldMatrix"),
                {}
              ).then((canvas) => {
                var dataURL = canvas.toDataURL("image/png");
                var link = document.createElement("a");
                link.download = "my-image.png";
                link.href = dataURL;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              });
            }}
          >
            保存感受野图片
          </Button>
        </div>
      );
    },
    // 叠加感受野
    renderMultiFieldGrayMatrixPreviewWithMapData() {
      const orient = "45.0";
      const scale = "13";
      const data = grayMatrixList[orient][scale];

      function getXInLowerScale(rowInd, colInd, highScale, lowScale) {
        const lowRowInd = rowInd - (highScale - lowScale) / 2;
        const lowColInd = colInd - (highScale - lowScale) / 2;
        return (grayMatrixList[orient][lowScale + ""][lowRowInd] || {})[
          lowColInd
        ];
      }

      return (
        <div>
          <div
            id="receptiveFieldMatrix"
            style={{
              width: "200px",
              height: "200px",
              background: "#fff",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              margin: "50px",
            }}
          >
            {data.map((row, rowInd) => {
              return (
                <div
                  style={{
                    width: "100%",
                    height: `${100 / data.length}%`,
                    display: "flex",
                  }}
                >
                  {row.map((_x, colInd) => {
                    const xList = Array(Math.floor("11" / 2))
                      .fill("")
                      .map((_, ind) =>
                        getXInLowerScale(
                          rowInd,
                          colInd,
                          parseInt(scale),
                          ind * 2 + 1
                        )
                      )
                      .filter((x) => x);
                    const x = Math.max(_x, ...xList);
                    return (
                      <div
                        style={{
                          height: "100%",
                          width: `${100 / row.length}%`,
                          background:
                            rowInd === Math.floor(data.length / 2) &&
                            colInd === Math.floor(data.length / 2)
                              ? "#1BA1E2"
                              : x === _x
                              ? `rgba(216,0,115,${x / 255})`
                              : `rgba(0,0,0,${x / 255})`,
                          border: "0.5px solid black",
                        }}
                      ></div>
                    );
                  })}
                </div>
              );
            })}
          </div>
          <Button
            type={"primary"}
            style={{ width: "100%" }}
            onClick={() => {
              html2canvas(
                document.querySelector("#receptiveFieldMatrix"),
                {}
              ).then((canvas) => {
                var dataURL = canvas.toDataURL("image/png");
                var link = document.createElement("a");
                link.download = "my-image.png";
                link.href = dataURL;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              });
            }}
          >
            保存叠加感受野图片
          </Button>
        </div>
      );
    },
    renderGrayMatrixPreviewWithListData() {
      const data = grayMatrixList[this.grayMatrixInd || 0];
      return (
        <div>
          <div
            id="receptiveFieldMatrix"
            style={{
              width: "200px",
              height: "200px",
              background: "#fff",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between",
              margin: "50px",
            }}
          >
            {data.map((row, rowInd) => (
              <div
                style={{
                  width: "100%",
                  height: `${100 / data.length}%`,
                  display: "flex",
                }}
              >
                {row.map((x, colInd) => (
                  <div
                    style={{
                      height: "100%",
                      width: `${100 / row.length}%`,
                      background:
                        rowInd === Math.floor(data.length / 2) &&
                        colInd === Math.floor(data.length / 2)
                          ? "#1BA1E2"
                          : `rgba(0,0,0,${x / 255})`,
                      // : `rgba(216,0,115,${x / 255})`,
                      border: "0.5px solid black",
                    }}
                  ></div>
                ))}
              </div>
            ))}
          </div>
          <div style={{ textAlign: "center", margin: "-20px 0 20px 0" }}>
            尺度：{data.length}
            <Button
              type={"primary"}
              style={{ width: "100%" }}
              onClick={() => {
                html2canvas(
                  document.querySelector("#receptiveFieldMatrix"),
                  {}
                ).then((canvas) => {
                  var dataURL = canvas.toDataURL("image/png");
                  var link = document.createElement("a");
                  link.download = "my-image.png";
                  link.href = dataURL;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                });
              }}
            >
              保存图片
            </Button>
          </div>
          <Slider
            style={{ width: "100%", margin: "-2px" }}
            dots={true}
            min={0}
            max={grayMatrixList.length - 1}
            value={this.grayMatrixInd}
            onChange={(i) => {
              this.grayMatrixInd = i;
            }}
          />
        </div>
      );
    },
    renderChartTooltip() {
      return (
        <div
          id="chart-tooltip"
          class="chart-tooltip"
          style={{
            visibility: this.showChartTooltip ? "visible" : "hidden",
          }}
        >
          {Object.entries(this.hoverChartBarData).map(([key, value]) => (
            <div>{`${key}: ${value}`}</div>
          ))}
        </div>
      );
    },
    redrawLayoutContent() {
      this.canRenderLayoutContent = false;
      setTimeout(() => {
        this.canRenderLayoutContent = true;
      }, 0);
    },
    onSearchNerveEditorSave(newVal) {
      this.options.searchNerveExpressions[
        this.options.searchNerveEditorInd
      ].content = newVal;
      this.updateOptions({
        searchNerveExpressions: this.options.searchNerveExpressions,
      });
    },
    renderSearchNerveEditor() {
      const editorContent =
        (
          this.options.searchNerveExpressions[
            this.options.searchNerveEditorInd
          ] || {}
        ).content || "";
      return (
        <Layout class="my-monaco-editor-layout">
          <Layout.Header class="common-layout-header">
            <div>
              <div
                class="layout-header-icon-box"
                onClick={() => {
                  this.updateLayoutContentSet(
                    "delete",
                    LAYOUT_CONTENT_NAMES.searchNerveEditor
                  );
                }}
              >
                <Icon
                  type="close"
                  class="layout-header-icon layout-header-icon-close"
                />
              </div>
              <div
                class="layout-header-icon-box"
                style={{
                  margin: 0,
                }}
                onClick={() => {
                  const editor = this.$refs.monacoEditor.getEditor();
                  this.onSearchNerveEditorSave(editor.getValue());
                  this.updateLayoutContentSet(
                    "delete",
                    LAYOUT_CONTENT_NAMES.searchNerveEditor
                  );
                }}
              >
                <Icon
                  type="save"
                  class="layout-header-icon layout-header-icon-save"
                />
              </div>
            </div>
          </Layout.Header>
          <Layout.Content>
            <MonacoEditor
              class="my-monaco-editor"
              theme="vs-dark"
              value={editorContent}
              language="python"
              ref="monacoEditor"
            />
          </Layout.Content>
        </Layout>
      );
    },
    renderBarChartContent(
      chartDatas = [],
      getBarTooltipExtinfo,
      onBarRightClick
    ) {
      {
        /* // debug
      const showSum = 4;
      const otherDatas = chartDatas.slice(showSum);
      chartDatas = chartDatas.slice(0, showSum).concat(Math.max(...otherDatas));
      // .concat(eval(otherDatas.join("+")) / otherDatas.length);
      console.log(666, eval(otherDatas.join("+")) / otherDatas.length); */
      }

      {
        /* const minChartDataValue = Math.min(...chartDatas); */
      }
      const minChartDataValue = -65;
      // 让数值最小的柱，也能在图表上露出来一点，便于观察
      const zeroOffset = Math.max(10 - minChartDataValue);
      {
        /* const zeroOffset = 0; */
      }
      const maxChartDataValue =
        Math.max(...chartDatas.map((data) => data + zeroOffset)) || 1;

      return (
        <Layout.Content>
          {/* 图表 */}
          <Layout
            style={{
              width: "100%",
              height: "100%",
            }}
          >
            {/* 图表y轴 */}
            <Layout.Sider
              style={{
                maxWidth: "fit-content",
                minWidth: "fit-content",
                padding: "10px",
                background: "transparent",
              }}
            ></Layout.Sider>
            <Layout>
              {/* 图表主体 */}
              <Layout.Content>
                {/* 图表内容 */}
                <div
                  class="bar-box"
                  id="barChartContent"
                  style={{ border: 0, padding: 0 }}
                >
                  {/* 图表柱 */}
                  {chartDatas.map((chartData, chartDataInd) => {
                    return (
                      <div
                        style={{
                          width: `${100 / chartDatas.length}%`,
                          height: "100%",
                          position: "relative",
                        }}
                      >
                        <div
                          style={{
                            width: "100%",
                            height: "100%",
                            display: "flex",
                            flexDirection: "row",
                            justifyContent: "space-around",
                            alignItems: "end",
                            padding: "0 15%",
                          }}
                        >
                          <div
                            style={{
                              width: `100%`,
                              height: `${
                                ((chartData + zeroOffset) / maxChartDataValue) *
                                100
                              }%`,
                              transition: "all .2s",
                              padding: "0 5%",
                              display: "flex",
                              alignItems: "end",
                            }}
                            onMouseenter={(e) => {
                              this.showChartTooltip = true;
                              this.hoverChartBarData = {
                                ...getBarTooltipExtinfo(chartDataInd),
                              };
                            }}
                            onMouseleave={(e) => {
                              this.showChartTooltip = false;
                            }}
                            onMousemove={(e) => {
                              const tooltipDom =
                                document.querySelector("#chart-tooltip");
                              tooltipDom.style.top = e.clientY + "px";
                              tooltipDom.style.left = e.clientX + "px";
                            }}
                            oncontextmenu={() =>
                              onBarRightClick && onBarRightClick(chartDataInd)
                            }
                          >
                            <div
                              style={{
                                width: "100%",
                                height: "100%",
                                backgroundColor: "tomato",
                                position: "relative",
                              }}
                            ></div>
                          </div>
                        </div>
                        <div
                          style={{
                            width: "12px",
                            position: "absolute",
                            left: "50%",
                            transform: "translate(-100%, -100%)",
                            pointerEvents: "none",
                            color: "#000",
                            lineHeight: "0px",
                            "writing-mode": "vertical-rl",
                          }}
                        >
                          {Object.entries(chartData)
                            .map(([prop, value]) => value)
                            .join(" ")}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </Layout.Content>
              {/* 图表x轴 */}
              <Layout.Footer
                style={{
                  maxHeight: "fit-content",
                  minHeight: "fit-content",
                  padding: "10px",
                  display: "flex",
                  flexDirection: "row",
                }}
              ></Layout.Footer>
            </Layout>
          </Layout>
        </Layout.Content>
      );
    },
    renderMatrixImage(allPropNames, showPropName) {
      const searchNerveExpression =
        this.options.searchNerveExpressions[this.options.searchNerveChartInd];
      const { chartSetting = {} } = searchNerveExpression;
      const searchNerveExpressionName = (
        searchNerveExpression.content || ""
      ).split("\n")[0];

      if (!chartSetting.contentInfos) {
        chartSetting.contentInfos = [
          {
            name: searchNerveExpressionName,
          },
        ];
        searchNerveExpression.chartSetting = chartSetting;
        this.updateOptions(
          {
            searchNerveExpressions: this.options.searchNerveExpressions,
          },
          false
        );

        return;
      }

      const imageSize = 280;
      const imageMargin = 20;
      const pixelWHSum = 28;
      const searchNerveResultMap = Object.fromEntries(
        this.options.searchNerveExpressions.map((expression, expressionInd) => [
          (expression.content || "").split("\n")[0],
          this.searchNerveResult[expressionInd],
        ])
      );

      return (
        <Layout.Content key={searchNerveExpressionName}>
          <Layout
            style={{
              width: "100%",
              height: "100%",
              position: "relative",
            }}
          >
            {/**矩阵列表 */}
            <Layout.Content>
              <div
                id="matrixList"
                style={{
                  width: `${imageSize}px`,
                  height: `${imageSize}px`,
                  margin: `${imageMargin}px`,
                  marginLeft: 0,
                }}
              >
                {chartSetting.contentInfos.map(
                  (contentInfo, contentInfoInd) => {
                    const expressionInfo =
                      searchNerveResultMap[contentInfo.name] || {};
                    const {
                      search_nerve_inds: searchNerveInds = [],
                      search_nerve_names: searchNerveNames = [],
                      search_nerve_prop_values: searchNervePropValues = {},
                      search_nerve_region_nos: searchNerveRegionNos = [],
                    } = expressionInfo;
                    const chartDatas =
                      searchNervePropValues[showPropName] || [];
                    const minChartDataValue = Math.min(...chartDatas);
                    const zeroOffset = Math.max(0 - minChartDataValue);
                    const maxChartDataValue = Math.max(
                      ...chartDatas.map((data) => data + zeroOffset)
                    );
                    const chartDatasSort = chartDatas
                      .slice()
                      .sort((a, b) => b - a);
                    const chartDatasArgSort = chartDatas.map((chartData) =>
                      chartDatasSort.indexOf(chartData)
                    );

                    {
                      /** 单个矩阵 */
                    }
                    return (
                      <div
                        style={{
                          width: `${imageSize}px`,
                          height: `${imageSize}px`,
                          marginLeft: `${
                            imageSize *
                              (chartSetting.contentInfoOffsets || [])[
                                contentInfoInd
                              ] || imageMargin
                          }px`,
                          float: "left",
                          position: "relative",
                          zIndex:
                            chartSetting.contentInfos.length - contentInfoInd,
                          boxShadow: "0px 0px 5px",
                        }}
                      >
                        {[...Array(pixelWHSum * pixelWHSum)].map(
                          (_, chartDataInd) => {
                            const chartData = chartDatas[chartDataInd];
                            const chartDatasArgSortInd =
                              chartDatasArgSort[chartDataInd];
                            const colorRatio =
                              (chartData + zeroOffset) /
                              (maxChartDataValue || 1);
                            const isHighlight =
                              chartDatasArgSortInd ===
                              contentInfo.highlightPixelIndex;
                            if (isHighlight && this.canAutoUpdateTooltip) {
                              setTimeout(() => {
                                pixelDom.elm.dispatchEvent(
                                  new Event("mouseenter")
                                );
                                const tooltipDom =
                                  document.querySelector("#chart-tooltip");
                                const pixelDomRect =
                                  pixelDom.elm.getBoundingClientRect();
                                tooltipDom.style.top =
                                  pixelDomRect.y +
                                  pixelDomRect.height / 2 +
                                  "px";
                                tooltipDom.style.left =
                                  pixelDomRect.x +
                                  pixelDomRect.width / 2 +
                                  "px";
                                this.canAutoUpdateTooltip = false;
                              }, 0);
                            }
                            const regionName = (
                              window.region[
                                searchNerveRegionNos[chartDataInd]
                              ] || {}
                            ).region_name;
                            const latexYX = `y=${
                              parseInt(chartDataInd / pixelWHSum) + 1
                            },x=${(chartDataInd % pixelWHSum) + 1}`;

                            // 正则表达式，匹配整数和小数
                            const regex = /-?\d+(\.\d+)?/g;
                            // 使用 match 方法来提取匹配的数字字符串
                            const matches = (
                              searchNerveNames[chartDataInd] || ""
                            ).match(regex);
                            // 将匹配的字符数组转换为数字数组
                            const numbers = matches ? matches.map(Number) : [];

                            const getTooltipExtinfo = (chartDataInd) => ({
                              // getTooltipExtinfo
                              region: regionName,
                              name: searchNerveNames[chartDataInd],
                              ind: searchNerveInds[chartDataInd],
                              latex: {
                                角: `Ang_{${latexYX}}^{o1=${numbers[0]},o2=${numbers[1]}}`,
                                轮廓中心: `Arc_{${latexYX}}`,
                              }[regionName],
                            });
                            const tooltipContent = {
                              ...getTooltipExtinfo(chartDataInd),
                              // [showPropName]: chartData,
                              ...Object.fromEntries(
                                allPropNames.map((propName) => [
                                  propName,
                                  (searchNervePropValues[propName] || {})[
                                    chartDataInd
                                  ],
                                ])
                              ),
                              pos: `${parseInt(chartDataInd / pixelWHSum)},${
                                chartDataInd % pixelWHSum
                              }`,
                            };

                            const [tickName, writeStageName, mnist] =
                              this.options.readFileName.split(";");
                            // TODO: 这个逻辑容易导致内存溢出 需要优化
                            {
                              /* if (
                              writeStageName === "attention_result" &&
                              isHighlight
                            ) {
                              this.recordSaccadeNode(
                                mnist,
                                tooltipContent.latex
                              );
                            } */
                            }

                            const exciteDotSize =
                              (imageSize / pixelWHSum) *
                              (contentInfo.zoom !== "auto"
                                ? contentInfo.zoom || 1
                                : tooltipContent.excite === -65
                                ? 0
                                : 0.8);

                            const pixelDom = (
                              <div
                                key={chartDataInd}
                                class="pixelDom"
                                style={{
                                  width: `${imageSize / pixelWHSum}px`,
                                  height: `${imageSize / pixelWHSum}px`,
                                  float: "left",
                                  display: "flex",
                                  justifyContent: "center",
                                  alignItems: "center",
                                }}
                                onMouseenter={(e) => {
                                  this.showChartTooltip = true;
                                  this.hoverChartBarData = tooltipContent;
                                }}
                                onMouseleave={(e) => {
                                  this.showChartTooltip = false;
                                }}
                                onMousemove={(e) => {
                                  const tooltipDom =
                                    document.querySelector("#chart-tooltip");
                                  tooltipDom.style.top = e.clientY + 10 + "px";
                                  tooltipDom.style.left = e.clientX + "px";
                                }}
                                onContextmenu={async () => {
                                  const nerveInd = tooltipContent.ind;
                                  const somaOrNerve = "soma";
                                  this.options.pinnedSomaInds.includes(nerveInd)
                                    ? this.deletePinnedInd(
                                        nerveInd,
                                        somaOrNerve
                                      )
                                    : this.updatePinnedSomaOrNerveInds(
                                        [nerveInd],
                                        somaOrNerve
                                      );
                                }}
                                onClick={async () => {
                                  {
                                    /* const { allNerveMap } = this; */
                                  }
                                  {
                                    /* const {
                                ind: nerveInd,
                                name: nerveName,
                                region: regionName,
                              } = tooltipContent;
                              
                              const nerveData = allNerveMap[nerveInd]; */
                                  }
                                  {
                                    /* console.log(nerveData,allNerveMap,chartDatas,tooltipContent) */
                                  }
                                  {
                                    /* const { region_row_no, region_hyper_col_no } =
                                nerveData;
                              const value = `\n(${region_row_no - 1}, ${
                                region_hyper_col_no - 1
                              }, '${regionName}', '${nerveName}', ${
                                searchNervePropValues["excite"][chartDataInd]
                              }),\n`; */
                                  }
                                  await navigator.clipboard.writeText(
                                    tooltipContent.latex
                                  );
                                  window.message.success("内容已复制");
                                }}
                              >
                                <div
                                  style={{
                                    ...(isHighlight
                                      ? {
                                          width: `${imageSize / pixelWHSum}px`,
                                          height: `${imageSize / pixelWHSum}px`,
                                          backgroundColor: `rgba(
                                      ${colorRatio * (contentInfo.R || 255)}, 
                                      ${colorRatio * (contentInfo.G || 255)}, 
                                      ${colorRatio * (contentInfo.B || 255)}, 
                                      ${contentInfo.A || 1}
                                    )`,
                                          border: `1px solid rgb(
                                      ${contentInfo.R || 255}, 
                                      ${contentInfo.G || 255}, 
                                      ${contentInfo.B || 255}
                                    )`,
                                        }
                                      : {
                                          width: `${exciteDotSize}px`,
                                          height: `${exciteDotSize}px`,
                                          backgroundColor: `rgba(
                                      ${colorRatio * (contentInfo.R || 255)}, 
                                      ${colorRatio * (contentInfo.G || 255)}, 
                                      ${colorRatio * (contentInfo.B || 255)}, 
                                      ${contentInfo.A || 1}
                                    )`,
                                        }),
                                  }}
                                ></div>
                              </div>
                            );
                            return pixelDom;
                          }
                        )}
                      </div>
                    );
                  }
                )}
              </div>
            </Layout.Content>
            {/* 侧边栏 */}
            <Layout.Sider>
              {/* 视图列表 */}
              <Space
                direction="vertical"
                style={{
                  width: "100%",
                  height: "100%",
                  float: "left",
                  overflow: "scroll",
                  background: "#fff",
                  padding: "8px",
                }}
              >
                {chartSetting.contentInfos.map(
                  (contentInfo, contentInfoInd) => (
                    <List
                      itemLayout="horizontal"
                      size="small"
                      bordered={true}
                      key={0}
                    >
                      {/* 按钮组 */}
                      <List.Item style={{ padding: 0 }}>
                        <Button.Group
                          style={{
                            display: "flex",
                            flexDirection: "row",
                            width: "100%",
                          }}
                        >
                          <Button
                            icon="plus"
                            style={{
                              width: "100%",
                              borderWidth: "0 1px 0 1px",
                              borderLeftWidth: 0,
                              borderRadius: "4px 0 0 0",
                            }}
                            onClick={() => {
                              chartSetting.contentInfos.splice(
                                contentInfoInd + 1,
                                0,
                                {}
                              );
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                          <Popconfirm
                            style={{
                              width: "100%",
                              borderWidth: "0 1px 0 1px",
                            }}
                            title="确认删除"
                            disabled={
                              contentInfo.name === searchNerveExpressionName
                            }
                            onConfirm={() => {
                              chartSetting.contentInfos.splice(
                                contentInfoInd,
                                1
                              );
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          >
                            <Button
                              icon="minus"
                              style={{
                                ...(contentInfo.name ===
                                searchNerveExpressionName
                                  ? {
                                      backgroundColor: "#f5f5f5",
                                      color: "rgba(0, 0, 0, 0.25)",
                                    }
                                  : {}),
                              }}
                            />
                          </Popconfirm>
                          <Button
                            icon="up"
                            style={{
                              width: "100%",
                              borderWidth: "0 1px 0 1px",
                            }}
                            onClick={() => {
                              const moveItem = chartSetting.contentInfos.splice(
                                contentInfoInd,
                                1
                              )[0];
                              chartSetting.contentInfos.splice(
                                contentInfoInd - 1,
                                0,
                                moveItem
                              );
                              this.updateOptions({
                                searchNerveExpressions:
                                  this.options.searchNerveExpressions,
                              });
                            }}
                          />
                          <Button
                            icon="down"
                            style={{
                              width: "100%",
                              borderWidth: "0 1px 0 1px",
                            }}
                            onClick={() => {
                              const moveItem = chartSetting.contentInfos.splice(
                                contentInfoInd,
                                1
                              )[0];
                              chartSetting.contentInfos.splice(
                                contentInfoInd + 1,
                                0,
                                moveItem
                              );
                              this.updateOptions({
                                searchNerveExpressions:
                                  this.options.searchNerveExpressions,
                              });
                            }}
                          />
                          <Button
                            icon="eye"
                            style={{
                              width: "100%",
                              borderWidth: "0 0px 0 1px",
                            }}
                            onClick={() => {
                              this.options.searchNerveExpressions[
                                searchNerveExpressionInd
                              ].isCompressed =
                                !this.options.searchNerveExpressions[
                                  searchNerveExpressionInd
                                ].isCompressed;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                        </Button.Group>
                      </List.Item>
                      {/* 名称 */}
                      <List.Item style={{ padding: 0 }}>
                        <Select
                          value={contentInfo.name}
                          disabled={
                            contentInfo.name === searchNerveExpressionName
                          }
                          style={{ border: 0, width: "100%" }}
                          class="noBorderSelect"
                          showArrow={false}
                          size="small"
                          onChange={(value) => {
                            chartSetting.contentInfos[contentInfoInd].name =
                              value;
                            this.options.searchNerveExpressions[
                              this.options.searchNerveChartInd
                            ].chartSetting = chartSetting;
                            this.updateOptions(
                              {
                                searchNerveExpressions:
                                  this.options.searchNerveExpressions,
                              },
                              false
                            );
                          }}
                        >
                          {this.options.searchNerveExpressions.map(
                            (expression) => {
                              const expressionName = (
                                expression.content || ""
                              ).split("\n")[0];
                              return (
                                <Select.Option value={expressionName}>
                                  {expressionName}
                                </Select.Option>
                              );
                            }
                          )}
                        </Select>
                      </List.Item>
                      {/**输入框组 */}
                      <List.Item style={{ padding: 0 }}>
                        <Input.Group compact style={{ display: "flex" }}>
                          <Input
                            placeholder="缩进"
                            style={{ borderWidth: "0 1px 0 0px" }}
                            value={
                              (chartSetting.contentInfoOffsets || [])[
                                contentInfoInd
                              ]
                            }
                            size="small"
                            onChange={(e) => {
                              // 希望缩进不和具体内容绑定，而是和列表索引绑定，所以用一个单独array维护
                              chartSetting.contentInfoOffsets =
                                chartSetting.contentInfoOffsets || [];
                              chartSetting.contentInfoOffsets[contentInfoInd] =
                                e.target.value;
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                          <Input
                            placeholder="缩放"
                            style={{
                              borderWidth: "0 0 0 1px",
                              borderRadius: 0,
                            }}
                            value={contentInfo.zoom}
                            size="small"
                            onChange={(e) => {
                              chartSetting.contentInfos[contentInfoInd].zoom =
                                e.target.value;
                              console.log("zoom", e.target.value);
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                        </Input.Group>
                      </List.Item>
                      <List.Item style={{ padding: 0 }}>
                        <Input.Group compact style={{ display: "flex" }}>
                          <Input
                            placeholder="R"
                            style={{ borderWidth: "0 1px 0 0" }}
                            value={contentInfo.R}
                            size="small"
                            onChange={(e) => {
                              chartSetting.contentInfos[contentInfoInd].R =
                                e.target.value;
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                          <Input
                            placeholder="G"
                            style={{ borderWidth: "0 1px 0 1px" }}
                            value={contentInfo.G}
                            size="small"
                            onChange={(e) => {
                              chartSetting.contentInfos[contentInfoInd].G =
                                e.target.value;
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                          <Input
                            placeholder="B"
                            style={{ borderWidth: "0 1px 0 1px" }}
                            value={contentInfo.B}
                            size="small"
                            onChange={(e) => {
                              chartSetting.contentInfos[contentInfoInd].B =
                                e.target.value;
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                          <Input
                            placeholder="A"
                            style={{ borderWidth: "0 0px 0 1px" }}
                            value={contentInfo.A}
                            size="small"
                            onChange={(e) => {
                              chartSetting.contentInfos[contentInfoInd].A =
                                e.target.value;
                              this.options.searchNerveExpressions[
                                this.options.searchNerveChartInd
                              ].chartSetting = chartSetting;
                              this.updateOptions(
                                {
                                  searchNerveExpressions:
                                    this.options.searchNerveExpressions,
                                },
                                false
                              );
                            }}
                          />
                        </Input.Group>
                      </List.Item>
                      {/* 高亮滑块 */}
                      <List.Item>
                        <Slider
                          style={{ width: "100%", margin: "-2px" }}
                          dots={true}
                          min={-1}
                          max={pixelWHSum * pixelWHSum - 1}
                          value={contentInfo.highlightPixelIndex}
                          onChange={(i) => {
                            this.canAutoUpdateTooltip = true;

                            chartSetting.contentInfos[
                              contentInfoInd
                            ].highlightPixelIndex = i;
                            this.options.searchNerveExpressions[
                              this.options.searchNerveChartInd
                            ].chartSetting = chartSetting;
                            this.updateOptions(
                              {
                                searchNerveExpressions:
                                  this.options.searchNerveExpressions,
                              },
                              false
                            );
                          }}
                        />
                      </List.Item>
                    </List>
                  )
                )}
                <Button
                  type={"primary"}
                  style={{ width: "100%" }}
                  onClick={() => {
                    html2canvas(document.querySelector("#matrixList"), {
                      x: imageMargin,
                      y: imageMargin,
                      width: imageSize,
                      height: imageSize,
                    }).then((canvas) => {
                      var dataURL = canvas.toDataURL("image/png");
                      var link = document.createElement("a");
                      link.download = `my-image.png`;
                      link.href = dataURL;
                      document.body.appendChild(link);
                      link.click();
                      document.body.removeChild(link);
                    });
                  }}
                >
                  保存矩阵图片
                </Button>
              </Space>
            </Layout.Sider>
          </Layout>
        </Layout.Content>
      );
    },
    renderSaccadePathway() {
      return (
        <div>
          <div
            id="saccadePathway"
            style={{
              display: "flex",
              flexWrap: "wrap",
            }}
          >
            {this.saccadePathList.map(([mnist, saccadePath], pathInd) => {
              const scale = 0.75;
              return (
                <div
                  id={`saccadePathway${pathInd}`}
                  style={{
                    position: "relative",
                    transformOrigin: "left top",
                    transform: `scale(${scale})`,
                    marginRight: `${280 * (scale - 1)}px`,
                    marginBottom: `${280 * (scale - 1)}px`,
                  }}
                >
                  <div
                    style={{
                      position: "absolute",
                      zIndex: 1,
                      fontSize: `${14 / scale}px`,
                    }}
                  >
                    &nbsp;{mnist}
                  </div>
                  {
                    <img
                      style={{
                        position: "absolute",
                        imageRendering: "pixelated",
                      }}
                      width={280}
                      height={280}
                      src={`/input/d28_mnist/${mnist}.bmp`}
                    />
                  }
                  {h(
                    "v-stage",
                    {
                      attrs: {
                        config: { width: 280, height: 280 },
                      },
                    },
                    [
                      h("v-layer", [
                        ...saccadePath.map((node) =>
                          h("v-" + node.type, {
                            attrs: { config: node.config },
                          })
                        ),
                      ]),
                    ]
                  )}
                </div>
              );
            })}
          </div>
          <Button
            onClick={() => {
              html2canvas(document.querySelector("#saccadePathway"), {}).then(
                (canvas) => {
                  var dataURL = canvas.toDataURL("image/png");
                  var link = document.createElement("a");
                  link.download = "my-image.png";
                  link.href = dataURL;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }
              );
              return;

              const start = 9 * 10;
              const end = 10 * 10;
              const targList = this.saccadePathList.slice(start, end);
              Promise.all(
                targList.map((_, pathInd) => {
                  pathInd = pathInd + start;
                  const canvas = html2canvas(
                    document.querySelector(`#saccadePathway${pathInd}`),
                    {}
                  );
                  console.log("[saccadePathList html2canvas]", pathInd);
                  return canvas;
                })
              )
                .then((canvasList) => {
                  this.zipDownloadBase64(
                    canvasList.map((canvas) => canvas.toDataURL()),
                    targList.map(([mnist, path]) => `saccade/path_${mnist}`),
                    "saccade"
                  );
                })
                .catch((e) => {
                  console.log(e);
                });
            }}
          >
            保存路径图片
          </Button>
        </div>
      );
    },
    renderCircuitTreeChart() {
      const allPropNames = this.options.showNerveProps;
      const showPropName = this.options.circuitTreeChartProp || allPropNames[0];
      const nextLeafNerveDatas = this.getNextNerveLeafDatas(
        this.options.nerveLeafChartNerveInd
      );
      const chartDatas = nextLeafNerveDatas.map(
        (data, dataInd) => data[showPropName]
      );

      return (
        <Layout
          class="barcharts-layout"
          style={{
            boxShadow: "rgb(1 1 1 / 30%) 0px 0px 10px",
          }}
        >
          <Layout.Header class="common-layout-header">
            <div
              class="layout-header-icon-box"
              onClick={() => {
                this.updateLayoutContentSet(
                  "delete",
                  LAYOUT_CONTENT_NAMES.circuitTreeChart
                );
              }}
            >
              <Icon
                type="close"
                class="layout-header-icon layout-header-icon-close"
              />
            </div>
            {/* <Checkbox.Group class="barcharts-props-checkboxgroup"
              options={allPropNames}
              value={showPropNames}
              onChange={(newVals) => {
                this.updateOptions({
                  circuitTreeChartProps: newVals,
                }, false)
              }}
            /> */}
            {/* 选择展示属性 */}
            <Radio.Group
              size="small"
              button-style="solid"
              value={this.options.circuitTreeChartProp}
              style={{}}
              onChange={(e) => {
                this.updateOptions(
                  {
                    circuitTreeChartProp: e.target.value,
                  },
                  false
                );
              }}
            >
              {allPropNames.map((propName) => (
                <Radio.Button value={propName}>{propName}</Radio.Button>
              ))}
            </Radio.Group>
          </Layout.Header>
          {/* 图表主体 */}
          {/* {this.renderBarChartContent(
            chartDatas,
            (chartDataInd) => {
              // getBarTooltipExtinfo
              const nerveData = nextLeafNerveDatas[chartDataInd];
              return {
                name: this.getNerveName(nerveData),
                ind: nerveData.ind,
                [this.options.circuitTreeChartProp]: chartDatas[chartDataInd],
              };
            },
            (chartDataInd) => {
              // onBarRightClick
              // const nerveData = chartDatas[chartDataInd];
              // const nerveInd = nerveData.ind;
              // this.updatePinnedSomaOrNerveInds([nerveInd], nerveData.type == 0 ? 'soma' : 'nerve')
            }
          )} */}
        </Layout>
      );
    },
    renderSearchNerveChart() {
      const searchNerveExpression =
        this.options.searchNerveExpressions[this.options.searchNerveChartInd];
      const { chartSetting = {}, chartShowProp } = searchNerveExpression;
      const { showType: chartContentType = "bar", radioOrCheckbox = "radio" } =
        chartSetting;
      const {
        search_nerve_inds: searchNerveInds = [],
        search_nerve_names: searchNerveNames = [],
        search_nerve_types: searchNerveTypes = [],
        search_nerve_prop_values: searchNervePropValues = {},
        search_nerve_region_nos: searchNerveRegionNos = [],
      } = this.searchNerveResult[this.options.searchNerveChartInd] || {};
      const allPropNames = [...Object.keys(searchNervePropValues)];
      const showPropName = chartShowProp || allPropNames[0];
      const chartDatas = searchNervePropValues[showPropName];

      return (
        <Layout
          class="barcharts-layout"
          style={{
            boxShadow: "rgb(1 1 1 / 30%) 0px 0px 10px",
          }}
        >
          <Layout.Header class="common-layout-header">
            <div
              class="layout-header-icon-box"
              onClick={() => {
                this.updateLayoutContentSet(
                  "delete",
                  LAYOUT_CONTENT_NAMES.searchNerveChart
                );
              }}
            >
              <Icon
                type="close"
                class="layout-header-icon layout-header-icon-close"
              />
            </div>
            {/* 选择展示属性 */}
            {radioOrCheckbox === "radio" ? (
              <div
                style={{
                  flexGrow: 1,
                  overflowX: "scroll",
                  height: "100%",
                  display: "grid",
                  alignItems: "center",
                }}
              >
                <Radio.Group
                  size="small"
                  button-style="solid"
                  value={searchNerveExpression.chartShowProp}
                  style={{
                    whiteSpace: "nowrap",
                    justifySelf: "center",
                    alignSelf: "center",
                  }}
                  onChange={(e) => {
                    searchNerveExpression.chartShowProp = e.target.value;
                    this.updateOptions(
                      {
                        searchNerveExpressions:
                          this.options.searchNerveExpressions,
                      },
                      false
                    );
                  }}
                >
                  {allPropNames.map((propName) => (
                    <Radio.Button value={propName}>{propName}</Radio.Button>
                  ))}
                </Radio.Group>
              </div>
            ) : (
              <div
                style={{ flexGrow: 1, overflowX: "scroll", display: "grid" }}
              >
                <Checkbox.Group
                  size="small"
                  button-style="solid"
                  value={searchNerveExpression.chartShowProp}
                  style={{
                    whiteSpace: "nowrap",
                    background: "white",
                    padding: "0 4px",
                    height: "24px",
                    borderRadius: "4px",
                    border: "1px solid #d9d9d9",
                    alignItems: "center",
                    justifySelf: "center",
                    alignSelf: "center",
                  }}
                  onChange={(newVal) => {
                    searchNerveExpression.chartShowProp = newVal;
                    this.updateOptions(
                      {
                        searchNerveExpressions:
                          this.options.searchNerveExpressions,
                      },
                      false
                    );
                  }}
                  options={allPropNames}
                ></Checkbox.Group>
              </div>
            )}
            {/* 单选/多选 */}
            <Radio.Group
              size="small"
              button-style="solid"
              value={radioOrCheckbox}
              style={{
                whiteSpace: "nowrap",
                marginLeft: "9px",
              }}
              onChange={(e) => {
                searchNerveExpression.chartSetting =
                  searchNerveExpression.chartSetting || {};
                searchNerveExpression.chartSetting.radioOrCheckbox =
                  e.target.value;
                this.updateOptions(
                  {
                    searchNerveExpressions: this.options.searchNerveExpressions,
                  },
                  false
                );
              }}
            >
              <Radio.Button value="radio">单</Radio.Button>
              <Radio.Button value="checkbox">多</Radio.Button>
            </Radio.Group>
            {/* 选择展示形式 */}
            <Radio.Group
              size="small"
              button-style="solid"
              value={chartContentType}
              style={{
                whiteSpace: "nowrap",
                marginLeft: "10px",
              }}
              onChange={(e) => {
                searchNerveExpression.chartSetting =
                  searchNerveExpression.chartSetting || {};
                searchNerveExpression.chartSetting.showType = e.target.value;
                this.updateOptions(
                  {
                    searchNerveExpressions: this.options.searchNerveExpressions,
                  },
                  false
                );
              }}
            >
              <Radio.Button value="bar">柱</Radio.Button>
              <Radio.Button value="image">图</Radio.Button>
            </Radio.Group>
            {chartContentType === "bar" && (
              <Button
                style={{
                  marginLeft: "10px",
                }}
                size="small"
                onClick={() => {
                  html2canvas(
                    document.querySelector("#barChartContent"),
                    {}
                  ).then((canvas) => {
                    var dataURL = canvas.toDataURL("image/png");
                    var link = document.createElement("a");
                    link.download = "my-image.png";
                    link.href = dataURL;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                  });
                }}
              >
                保存柱状图
              </Button>
            )}
            {this.readFileName.split(";")[1] === "back_propagation_to_dot" && (
              <Button
                style={{
                  marginLeft: "10px",
                }}
                size="small"
                onClick={() => {
                  this.zipDownloadBase64(
                    Object.values(this.backPropagationBase64Map)
                      .map((base64List) => base64List)
                      .flat(),
                    Object.entries(this.backPropagationBase64Map)
                      .map(([mnist, base64List]) =>
                        base64List.map((_, ind) => `${mnist}/${ind}`)
                      )
                      .flat(),
                    "back_propagation"
                  );

                  html2canvas(
                    document.querySelector("#barChartContent"),
                    {}
                  ).then((canvas) => {
                    var dataURL = canvas.toDataURL("image/png");
                    var link = document.createElement("a");
                    link.download = "my-image.png";
                    link.href = dataURL;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                  });
                }}
              >
                批量保存反向传播图
              </Button>
            )}
          </Layout.Header>
          {/* 图表主体 */}
          {/* 柱状图 */}
          {chartContentType == "bar" &&
            this.renderBarChartContent(
              chartDatas,
              (chartDataInd) => {
                return {
                  // getBarTooltipExtinfo
                  name: searchNerveNames[chartDataInd],
                  ind: searchNerveInds[chartDataInd],
                  // [showPropName]: chartDatas[chartDataInd],
                  ...Object.fromEntries(
                    allPropNames.map((propName) => [
                      propName,
                      searchNervePropValues[propName][chartDataInd],
                    ])
                  ),
                };
              },
              (chartDataInd) => {
                // onBarRightClick
                const nerveInd = searchNerveInds[chartDataInd];
                const nerveType = searchNerveTypes[chartDataInd];
                const somaOrNerve = nerveType == 2 ? "nerve" : "soma";
                this.options.pinnedSomaInds.includes(nerveInd)
                  ? this.deletePinnedInd(nerveInd, somaOrNerve)
                  : this.updatePinnedSomaOrNerveInds([nerveInd], somaOrNerve);
              }
            )}
          {/* 图片 */}
          {chartContentType === "image" &&
            this.renderMatrixImage(allPropNames, showPropName)}
        </Layout>
      );
    },
    renderFilterPanel() {
      return (
        <Space
          align="start"
          direction="horizontal"
          style={{
            width: "100%",
          }}
        >
          <Form
            style={
              {
                // paddingBottom: DRAWER_PADDING_BOTTOM,
              }
            }
            labelCol={{}}
          >
            <Form.Item label="胞体属性">
              {this.renderSelector({
                options: this.allProps,
                value: this.options.showSomaProps,
                onChange: (data) => {
                  this.updateOptions(
                    {
                      showSomaProps: data,
                    },
                    false
                  );
                },
              })}
            </Form.Item>
            <Form.Item label="神经突属性">
              {this.renderSelector({
                options: this.allProps,
                value: this.options.showNerveProps,
                onChange: (data) =>
                  this.updateOptions(
                    {
                      showNerveProps: data,
                    },
                    false
                  ),
              })}
            </Form.Item>
            <Form.Item label="时间节点过滤">
              {this.renderSelector({
                options: [
                  ...new Set(
                    this.allFileName.map((name) => name.split(";")[1])
                  ),
                ],
                value: this.options.onlyShowHistoryFileNames,
                onChange: (data) => {
                  this.updateOptions(
                    {
                      onlyShowHistoryFileNames: data,
                    },
                    false
                  );
                },
              })}
              <Input
                addonBefore="正则"
                size="small"
                value={this.options.historyFileNamesRegStr}
                onPressEnter={(e) => {
                  this.updateOptions(
                    {
                      historyFileNamesRegStr: e.target.value,
                    },
                    false
                  );
                }}
              />
            </Form.Item>
            <Form.Item label="钉住的胞体">
              <Space direction="vertical" style={{ width: "100%" }}>
                {this.renderPinnedList(
                  "soma",
                  this.options.pinnedSomaInds,
                  (addInds) => {
                    this.updatePinnedSomaOrNerveInds(addInds, "soma");
                  }
                )}
                <Radio.Group
                  style={{ width: "100%" }}
                  value={this.options.showPinnedSomaNerveType}
                  onChange={(e) => {
                    const data = e.target.value;
                    this.updateOptions({ showPinnedSomaNerveType: data });
                  }}
                >
                  {["in", "out", "all"].map((value) => (
                    <Radio.Button
                      key={value}
                      value={value}
                      style={{ width: `${(1 / 3) * 100}%` }}
                    >
                      {value}
                    </Radio.Button>
                  ))}
                </Radio.Group>
                <Switch
                  checked={this.options.isShowPinnedSomaCircuit}
                  checkedChildren="只展示钉住的胞体的神经回路"
                  unCheckedChildren="只展示钉住的胞体的神经回路"
                  style={{ width: "100%" }}
                  onClick={() =>
                    this.updateOptions({
                      isShowPinnedSomaCircuit:
                        !this.options.isShowPinnedSomaCircuit,
                    })
                  }
                />
                <Switch
                  checked={
                    this.options.layoutContentSet.slice(-1)[0] ===
                    LAYOUT_CONTENT_NAMES.circuitTreePanel
                  }
                  checkedChildren="展示钉住的胞体的神经回路树状图"
                  unCheckedChildren="展示钉住的胞体的神经回路树状图"
                  style={{ width: "100%" }}
                  onClick={(checked) => {
                    this.updateLayoutContentSet(
                      checked ? "moveToEnd" : "delete",
                      LAYOUT_CONTENT_NAMES.circuitTreePanel
                    );
                  }}
                />
              </Space>
            </Form.Item>
            <Form.Item label="钉住的神经突">
              <Space direction="vertical" style={{ width: "100%" }}>
                {this.renderPinnedList(
                  "nerve",
                  this.options.pinnedNerveInds,
                  (addInds) => {
                    // addIndCallback
                    this.updatePinnedSomaOrNerveInds(addInds, "nerve");
                    // this.updateOptions({
                    //   pinnedNerveInds: [...new Set([...this.options.pinnedNerveInds || [], ...addInds])],
                    // })
                  }
                )}
                <Switch
                  checked={this.options.isOnlyShowPinnedNerves}
                  checkedChildren="只展示钉住的神经突"
                  unCheckedChildren="展示所有的神经突"
                  style={{ width: "100%" }}
                  onClick={() =>
                    this.updateOptions({
                      isOnlyShowPinnedNerves:
                        !this.options.isOnlyShowPinnedNerves,
                    })
                  }
                />
              </Space>
            </Form.Item>
            {/* <Form.Item>
              <Input
                addonBefore="只展示LTP大于"
                addonAfter="的突触"
                style={{
                  width: "100%",
                  textAlign: 'center'
                }}
                value={this.options.minLTPThreshold}
                onPressEnter={(e) => {
                  this.updateOptions({
                    minLTPThreshold: e.target.value
                  });
                }}
              />
            </Form.Item> */}
            {/* <Form.Item>
              <Input.Group style={{
                width: '100%',
                display: 'flex',
                flexDirection: 'row',
              }}>
                <Input
                  style="border-right: 0; pointer-events: none; background-color: #fff;color:#000;"
                  placeholder="回路长度"
                  disabled
                />
                <Input
                  value={this.options.minCircuitLength}
                  style={{
                    textAlign: "center"
                  }}
                  placeholder="Minimum"
                  onPressEnter={(e) => {
                    this.updateOptions({
                      minCircuitLength: e.target.value
                    });
                  }}
                />
                <Input
                  style="width:30px;border-left: 0;border-right: 0; pointer-events: none; background-color: #fff"
                  placeholder="~"
                  disabled
                />
                <Input
                  value={this.options.maxCircuitLength}
                  style={{
                    textAlign: "center"
                  }}
                  placeholder="Maximum"
                  onPressEnter={(e) => {
                    this.updateOptions({
                      maxCircuitLength: e.target.value
                    });
                  }}
                />
              </Input.Group>
            </Form.Item> */}
            {/* <Form.Item>
              <Input
                addonBefore="只展示前"
                addonAfter="个最强的突触"
                value={this.options.onlyShowTopNSynapses}
                style={{
                  textAlign: 'center',
                }}
                onPressEnter={(e) => {
                  this.updateOptions({
                    onlyShowTopNSynapses: e.target.value,
                  });
                }}
              />
            </Form.Item> */}
            <Form.Item>
              <Radio.Group
                value={this.options.layoutSize}
                style={{
                  width: "100%",
                  display: "flex",
                }}
                onChange={(e) => {
                  this.updateOptions({
                    layoutSize: e.target.value,
                  });
                }}
              >
                <Radio.Button value="disabled" disabled style={{}}>
                  布局尺寸
                </Radio.Button>
                <Radio.Button
                  value="normal"
                  style={{
                    textAlign: "center",
                    flex: 1,
                  }}
                >
                  标准
                </Radio.Button>
                <Radio.Button
                  value="small"
                  style={{
                    textAlign: "center",
                    flex: 1,
                  }}
                >
                  小
                </Radio.Button>
                <Radio.Button
                  value="extreme_small"
                  style={{
                    textAlign: "center",
                    flex: 1,
                  }}
                >
                  极小
                </Radio.Button>
              </Radio.Group>
            </Form.Item>
          </Form>
        </Space>
      );
    },
    updatePinnedSomaOrNerveInds(addInds, somaOrNerve) {
      switch (somaOrNerve) {
        case "soma":
          this.updateOptions({
            pinnedSomaInds: [
              ...new Set([...(this.options.pinnedSomaInds || []), ...addInds]),
            ],
          });
          break;
        case "nerve":
          this.updateOptions({
            pinnedNerveInds: [
              ...new Set([...(this.options.pinnedNerveInds || []), ...addInds]),
            ],
          });
          break;
      }
    },
    renderElevatorPanel() {
      return (
        <Tabs
          class="elevator-tab"
          style={{
            height: "100%",
            width: "100%",
            display: "flex",
            flexDirection: "column",
          }}
          activeKey={this.options.leftDrawerTabsActiveKey}
          onChange={(activeKey) =>
            this.updateOptions({ leftDrawerTabsActiveKey: activeKey }, false)
          }
        >
          <Tabs.TabPane key="1" tab="楼层导航">
            <Space
              direction="vertical"
              style={{
                width: "100%",
                height: "85vh",
                float: "left",
                overflow: "scroll",
              }}
            >
              <Collapse
                accordion
                style={{
                  width: "100%",
                }}
                activeKey={this.options.elevatorRegion}
                onChange={(regionName) => {
                  this.gotoElevator(regionName);
                  // this.gotoElevator(region_name, elevatorAnchor)
                }}
              >
                {Object.values(window.region).map((region) => {
                  const { region_name } = region;
                  const updateRegion = this.updateRegion(region);
                  return (
                    <Collapse.Panel
                      key={region_name}
                      header={region_name}
                      showArrow={false}
                      extra={[
                        ...(this.appMode === "edit"
                          ? [
                              <Icon
                                type="save"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  this.saveRegion(region);
                                }}
                              />,
                              <Divider type="vertical" />,
                              <Icon
                                type="delete"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  this.deleteRegion(region);
                                }}
                              />,
                              <Divider type="vertical" />,
                            ]
                          : []),
                        this.options.hideRegions.includes(region_name) ? (
                          <Icon
                            type="eye-invisible"
                            onClick={(e) =>
                              e.stopPropagation() & this.showRegion(region_name)
                            }
                          />
                        ) : (
                          <Icon
                            type="eye"
                            onClick={(e) =>
                              e.stopPropagation() & this.hideRegion(region_name)
                            }
                          />
                        ),
                      ]}
                    >
                      <Space
                        direction="vertical"
                        style={{
                          width: "100%",
                        }}
                      >
                        {this.renderElevatorRegionAnchorInput(region)}
                        {this.renderElevatorRegionHighlightNeuronRegExpInput(
                          region
                        )}
                      </Space>
                    </Collapse.Panel>
                  );
                })}
              </Collapse>
            </Space>
          </Tabs.TabPane>
          <Tabs.TabPane key="2" tab="搜索">
            {this.renderSearchNervePanel()}
          </Tabs.TabPane>
        </Tabs>
      );
    },
    renderSearchNervePanel() {
      const { searchNerveResult } = this;
      const getSearchNerveData = (
        ind,
        searchNerveNames,
        searchNervePropValues
      ) => {
        const nerveName = searchNerveNames[ind];
        const title = `${nerveName}`;
        const nerveData = (
          <div key={nerveName} class="nerve-tree-node">
            <div
              slot="title"
              oncontextmenu={(e) =>
                this.onCircuitTreeLeafContextmenu(e, nerveData)
              }
            >
              {title}&nbsp;&nbsp;
              {Object.keys(searchNervePropValues).map((key) => (
                <Tooltip title={key}>
                  <Tag color="">{searchNervePropValues[key][ind]}</Tag>
                </Tooltip>
              ))}
            </div>
          </div>
        );
        return nerveData;
      };

      return (
        <Space
          direction="vertical"
          style={{
            width: "100%",
            height: "85vh",
            float: "left",
            overflow: "scroll",
          }}
        >
          {(this.options.searchNerveExpressions.length > 0
            ? this.options.searchNerveExpressions
            : [""]
          ).map((searchNerveExpression, searchNerveExpressionInd) => {
            const {
              message,
              search_nerve_inds: searchNerveInds = [],
              search_nerve_names: searchNerveNames = [],
              search_nerve_prop_values: searchNervePropValues = {},
            } = searchNerveResult[searchNerveExpressionInd] || {};

            return (
              <List
                itemLayout="horizontal"
                size="small"
                bordered={true}
                key={searchNerveExpression.content}
                style={{
                  borderColor:
                    this.options.searchNerveChartInd == searchNerveExpressionInd
                      ? "black"
                      : null,
                }}
              >
                <List.Item style={{ padding: 0 }}>
                  <Button.Group
                    style={{
                      display: "flex",
                      flexDirection: "row",
                      width: "100%",
                    }}
                  >
                    <Button
                      icon="plus"
                      style={{
                        width: "100%",
                        borderWidth: "0 1px 0 1px",
                        borderLeftWidth: 0,
                        borderRadius: "4px 0 0 0",
                      }}
                      onClick={() => {
                        this.options.searchNerveExpressions.splice(
                          searchNerveExpressionInd + 1,
                          0,
                          {}
                        );
                        this.updateOptions({
                          searchNerveExpressions:
                            this.options.searchNerveExpressions,
                        });
                      }}
                    />
                    <Popconfirm
                      style={{ width: "100%", borderWidth: "0 1px 0 1px" }}
                      title="确认删除"
                      onConfirm={() => {
                        this.options.searchNerveExpressions.splice(
                          searchNerveExpressionInd,
                          1
                        );
                        this.updateOptions({
                          searchNerveExpressions:
                            this.options.searchNerveExpressions,
                        });
                      }}
                    >
                      <Button icon="minus" />
                    </Popconfirm>
                    <Button
                      icon="up"
                      style={{ width: "100%", borderWidth: "0 1px 0 1px" }}
                      onClick={() => {
                        const moveItem =
                          this.options.searchNerveExpressions.splice(
                            searchNerveExpressionInd,
                            1
                          )[0];
                        this.options.searchNerveExpressions.splice(
                          searchNerveExpressionInd - 1,
                          0,
                          moveItem
                        );
                        this.updateOptions({
                          searchNerveExpressions:
                            this.options.searchNerveExpressions,
                        });
                      }}
                    />
                    <Button
                      icon="down"
                      style={{ width: "100%", borderWidth: "0 1px 0 1px" }}
                      onClick={() => {
                        const moveItem =
                          this.options.searchNerveExpressions.splice(
                            searchNerveExpressionInd,
                            1
                          )[0];
                        this.options.searchNerveExpressions.splice(
                          searchNerveExpressionInd + 1,
                          0,
                          moveItem
                        );
                        this.updateOptions({
                          searchNerveExpressions:
                            this.options.searchNerveExpressions,
                        });
                      }}
                    />
                    <Button
                      icon={
                        searchNerveExpression.isCompressed
                          ? "arrows-alt"
                          : "shrink"
                      }
                      style={{ width: "100%", borderWidth: "0 1px 0 1px" }}
                      onClick={() => {
                        this.options.searchNerveExpressions[
                          searchNerveExpressionInd
                        ].isCompressed =
                          !this.options.searchNerveExpressions[
                            searchNerveExpressionInd
                          ].isCompressed;
                        this.updateOptions(
                          {
                            searchNerveExpressions:
                              this.options.searchNerveExpressions,
                          },
                          false
                        );
                      }}
                    />
                    <Button
                      icon="bar-chart"
                      type="primary"
                      style={{
                        width: "100%",
                        borderWidth: "0 1px 0 1px",
                        borderRightWidth: 0,
                        borderRadius: "0 4px 0 0",
                      }}
                      onClick={() => {
                        // 以柱状图形式查看搜索结果
                        this.updateOptions({
                          searchNerveChartInd: searchNerveExpressionInd,
                        });
                        this.updateLayoutContentSet(
                          "moveToEnd",
                          LAYOUT_CONTENT_NAMES.searchNerveChart
                        );
                      }}
                    />
                  </Button.Group>
                </List.Item>
                <List.Item
                  style={{
                    padding: 0,
                  }}
                >
                  <Input.TextArea
                    value={(searchNerveExpression.content || "").split("\n")[0]}
                    style={{
                      padding: "8px 16px",
                      width: "100%",
                      minHeight: "34px",
                      maxHeight: "34px",
                      borderWidth: 0,
                      borderColor: "transparent",
                      overflow: "hidden",
                      backgroundColor: "transparent",
                    }}
                    onFocus={(e) => {
                      this.updateLayoutContentSet(
                        "moveToEnd",
                        LAYOUT_CONTENT_NAMES.searchNerveEditor
                      );
                      this.updateOptions(
                        {
                          searchNerveEditorInd: searchNerveExpressionInd,
                        },
                        false
                      );
                      this.searchNerveEditorContent = e.target.value;
                    }}
                  />
                </List.Item>
                {searchNerveInds.length > 0 &&
                !this.options.searchNerveExpressions[searchNerveExpressionInd]
                  .isCompressed ? (
                  searchNerveInds.map((nerveInd, ind) => (
                    <List.Item>
                      {getSearchNerveData(
                        ind,
                        searchNerveNames,
                        searchNervePropValues
                      )}
                    </List.Item>
                  ))
                ) : (
                  <List.Item>{message}</List.Item>
                )}
              </List>
            );
          })}
        </Space>
      );
    },
    updateLayoutContentSet(updateType, contentName) {
      const UPDATE_TYPE = {
        moveToEnd: "moveToEnd",
        delete: "delete",
        add: "add",
      };
      const layoutContentSet = new Set(this.options.layoutContentSet);

      switch (updateType) {
        case UPDATE_TYPE.moveToEnd:
          layoutContentSet.delete(contentName);
          layoutContentSet.add(contentName);
          break;
        case UPDATE_TYPE.delete:
          layoutContentSet.delete(contentName);
          break;
        case UPDATE_TYPE.add:
          layoutContentSet.add(contentName);
          break;
      }

      this.updateOptions(
        {
          layoutContentSet: [...layoutContentSet],
        },
        false
      );
    },
    renderElevatorRegionAnchorInput(region) {
      const { region_name } = region;
      const elevatorAnchor =
        (this.options.elevatorAnchor || {})[region_name] || {};
      return (
        <Input.Group compact style={{ width: "100%" }}>
          <InputNumber
            style={{ width: "35%" }}
            placeholder="row"
            value={elevatorAnchor.rowNo}
            onChange={(rowNo) =>
              this.gotoElevator(region_name, {
                ...elevatorAnchor,
                rowNo,
              })
            }
          />
          <InputNumber
            style={{ width: "35%" }}
            placeholder="col"
            value={elevatorAnchor.colNo}
            onChange={(colNo) =>
              this.gotoElevator(region_name, {
                ...elevatorAnchor,
                colNo,
              })
            }
          />
          <Button
            style={{ width: "30%" }}
            type="primary"
            onClick={() => this.gotoElevator(region_name, elevatorAnchor)}
          >
            GO
          </Button>
        </Input.Group>
      );
    },
    renderElevatorRegionOffsetInput(region) {
      const { region_name } = region;
      return (
        <Input
          placeholder="脑区X轴偏移量"
          value={this.options.regionOffsetX[region_name]}
          onPressEnter={(e) => {
            this.changeRegionOffsetX(region_name, e.target.value);
          }}
        />
      );
    },
    exchangeRegExp(exp) {
      return exp
        .replace(/（/g, "(")
        .replace(/）/g, ")")
        .replace(/ /g, ".*")
        .replace(/【/g, "^")
        .replace(/】/g, "$")
        .replace(/、/g, "|");
    },
    renderElevatorRegionHighlightNeuronRegExpInput(region) {
      const { region_name } = region;
      const onPressEnter = (e) => {
        const regExp = this.exchangeRegExp(e.target.value);
        this.changeRegionHighlightNeuronRegExp(region_name, regExp);
      };
      return (
        <Input
          placeholder="正则过滤"
          allowClear
          value={this.options.regionHighlightNeuronRegExp[region_name]}
          onPressEnter={onPressEnter}
        />
      );
    },
    renderElevatorRegionBaseForm(region, updateRegion) {
      const { raw_region_json } = region;
      let region_shape = raw_region_json["region_shape"];
      return (
        <Form layout="inline">
          <Form.Item label="脑区名称">
            <Input
              value={raw_region_json["region_name"]}
              onBlur={(e) => {
                updateRegion({ region_name: e.target.value });
              }}
            />
          </Form.Item>
          <Form.Item label="脑区尺寸">
            <Input.Group style={{ width: "100%" }} compact>
              <InputNumber
                placeholder="行数"
                style={{ width: `${(1 / 3) * 100}%` }}
                value={raw_region_json["region_shape"][0]}
                onChange={(val) => {
                  region_shape[0] = val;
                  updateRegion({ region_shape });
                }}
              />
              <InputNumber
                placeholder="超柱数"
                value={raw_region_json["region_shape"][1]}
                style={{ width: `${(1 / 3) * 100}%` }}
                onChange={(val) => {
                  region_shape[1] = val;
                  updateRegion({ region_shape });
                }}
              />
              <InputNumber
                placeholder="微柱数"
                value={raw_region_json["region_shape"][2]}
                style={{ width: `${(1 / 3) * 100}%` }}
                onChange={(val) => {
                  region_shape[2] = val;
                  updateRegion({ region_shape });
                }}
              />
            </Input.Group>
          </Form.Item>
        </Form>
      );
    },
    renderPinnedList(pinnedType, data = [], addIndCallback) {
      return (
        <List itemLayout="horizontal" size="small" bordered={true}>
          {data.map(
            ((pinnedId) => {
              return (
                <List.Item
                  class="pinned-list-item"
                  extra={
                    <Icon
                      type="close"
                      onClick={() => {
                        this.deletePinnedInd(pinnedId, pinnedType);
                      }}
                    />
                  }
                >
                  {pinnedId}
                  {/* <Input
                    addonBefore="限制回路长度"
                    size="small"
                    style={{
                      textAlign: 'center',
                      margin: "0 20px",
                    }}
                    value={(this.options.pinnedSomaShowMaxCircuitLengthMap || {})[pinnedId]}
                    onPressEnter={(e) => {
                      const { pinnedSomaShowMaxCircuitLengthMap = {} } = this.options;
                      pinnedSomaShowMaxCircuitLengthMap[pinnedId] = e.target.value;
                      this.updateOptions({
                        pinnedSomaShowMaxCircuitLengthMap,
                      });
                    }}
                  /> */}
                </List.Item>
              );
            }).bind(this)
          )}
          {data.length > 0 ? (
            <List.Item
              class="pinned-list-item"
              style="text-align:center;"
              onClick={() => {
                this.deletePinnedInd("all", pinnedType);
              }}
            >
              清空
            </List.Item>
          ) : (
            ""
          )}
          <Input
            placeholder="添加"
            value={this.manuallyAddPinnedSomaOrNervesStr}
            style={{
              borderWidth: 0,
              borderColor: "transparent",
              height: "38px",
              fontSize: "14px",
              padding: "8px 16px",
            }}
            onPressEnter={(e) => {
              const inds = e.target.value
                .split(" ")
                .map((val) => parseInt(val))
                .filter((val) => !isNaN(val));
              addIndCallback(inds);
              this.manuallyAddPinnedSomaOrNervesStr = "";
            }}
          />
        </List>
      );
    },
    deletePinnedInd(pinnedId, pinnedType) {
      const updateKey = {
        soma: "pinnedSomaInds",
        nerve: "pinnedNerveInds",
      }[pinnedType];
      const originDatas = new Set(this.options[updateKey]);
      if (pinnedId === "all") {
        originDatas.clear();
      } else {
        originDatas.delete(pinnedId);
      }
      this.updateOptions({
        [updateKey]: [...originDatas],
      });
    },
    renderTimelineSlider() {
      return (
        <div class="slider-box">
          <Slider
            tooltipVisible={this.showTimelineTooltips}
            tooltipPlacement={"left"}
            style={{ width: "100%", margin: "14px" }}
            dots={true}
            max={this.historyFiles.length - 1}
            value={this.historyFiles.findIndex(
              (fileName) => fileName == this.options.readFileName
            )}
            tipFormatter={(i) => {
              return this.historyFiles[i];
            }}
            onChange={(i) => this.setReadFileName(this.historyFiles[i])}
            onFocus={() => {
              this.showTimelineTooltips = true;
            }}
            onBlur={() => {
              this.showTimelineTooltips = undefined;
            }}
          />
          {
            <Input
              class="timeline-search"
              placeholder="正则搜索"
              onPressEnter={(e) => {
                const searchReg = RegExp(
                  `^${this.exchangeRegExp(e.target.value)}`
                );
                const historyFile = this.historyFiles.find((fileName) =>
                  searchReg.test(fileName)
                );
                this.setReadFileName(historyFile);
              }}
            />
          }
        </div>
      );
    },
    renderTag(value, propName) {
      return (
        <Tooltip title={propName || value}>
          <Tag
            color=""
            onClick={async () => {
              await navigator.clipboard.writeText(value);
              window.message.success("内容已复制");
            }}
            onContextmenu={(e) => {
              e.stopPropagation();
              e.preventDefault();
              if (["ind", "soma_ind", "pre_ind"].includes(propName)) {
                const pinInd = value;
                this.options.pinnedSomaInds.includes(pinInd)
                  ? this.deletePinnedInd(pinInd, "soma")
                  : this.updatePinnedSomaOrNerveInds([pinInd], "soma");
              }
            }}
          >
            {value}
          </Tag>
        </Tooltip>
      );
    },
    getNextNerveLeafDatas(nerveInd) {
      const { allNerveMap } = this;
      const nerveData = allNerveMap[nerveInd];
      let nextLeafNerveDatas = null;

      switch (this.options.showPinnedSomaNerveType) {
        case "in":
        case "all":
          nextLeafNerveDatas = Object.values(allNerveMap).filter(
            (nerve) => nerve.post_ind === nerveInd
          );
          break;
        case "out":
          nextLeafNerveDatas = [
            ...Object.values(allNerveMap).filter(
              (nerve) => nerve.pre_ind === nerveInd
            ),
            ...Object.values(allNerveMap).filter(
              (nerve) => nerve.ind === nerveData.post_ind
            ),
          ].sort((nerve0, nerve1) => nerve0.ind - nerve1.ind);
          break;
      }

      nextLeafNerveDatas = nextLeafNerveDatas.sort(
        (d1, d2) => d1.pre_ind - d2.pre_ind
      );

      return nextLeafNerveDatas;
    },
    getNerveName(nerveData) {
      const nerveRegion = region[nerveData.region_no] || {};
      const nerveName = (
        Object.values(nerveRegion.neurons || {}).find(
          (neuronInfo) => neuronInfo.neuron_no === nerveData.neuron_no
        ) || {}
      ).name;
      console.log("[getNerveName]", nerveData, nerveRegion, region);
      return nerveName;
    },
    renderCircuitTreePanel() {
      const { somasMap, allNerveMap, options, cortexConsts = {} } = this;
      const { type: nerveType = {} } = cortexConsts;
      const allNerveInds = [];
      const getNerveLeafData = (nerveInd) => {
        allNerveInds.push(nerveInd);

        const nerveData = allNerveMap[nerveInd] || {};
        // type===2的是axon_end或synapse
        const isSynapse = [
          nerveType.axon_end,
          nerveType.spine_connect,
        ].includes(nerveData.type);
        const somaOrNerve = isSynapse ? "nerve" : "soma";
        const showProps =
          {
            soma: options.showSomaProps,
            nerve: options.showNerveProps,
          }[somaOrNerve] || [];
        const somaData =
          somaOrNerve === "nerve"
            ? somasMap[nerveData.pre_ind] || {}
            : nerveData;

        const regionName = (region[somaData.region_no] || {}).region_name;
        const somaName = this.getNerveName(somaData);

        const nextLeafNerveDatas = this.getNextNerveLeafDatas(nerveInd);
        // const title = `${somaName} ${isSynapse ? '[S]' : ''}`;
        nextLeafNerveDatas.sort((a, b) => a.ind - b.ind);
        const title = `【${regionName}】${somaName}`;
        const TreeNode = Tree.TreeNode;
        const PROP_VALUE_MAX_TOFIXED = 3;
        const leafData = (
          <TreeNode key={nerveInd} class="nerve-tree-node">
            <div
              slot="title"
              oncontextmenu={(e) =>
                this.onCircuitTreeLeafContextmenu(e, nerveData)
              }
            >
              {title}&nbsp;&nbsp;
              {showProps.map((prop) => {
                const tagValue =
                  (String(nerveData[prop]).split(".")[1] || {}).length >
                  PROP_VALUE_MAX_TOFIXED
                    ? parseFloat(nerveData[prop]).toFixed(
                        PROP_VALUE_MAX_TOFIXED
                      )
                    : nerveData[prop];
                return this.renderTag(tagValue, prop);
              })}
              <Tag
                onClick={() => {
                  // 查看叶子节点的柱状图
                  // this.nerveLeafsChartData = nextLeafNerveDatas;
                  this.updateOptions(
                    {
                      nerveLeafChartNerveInd: nerveData.ind,
                    },
                    false
                  );
                  this.updateLayoutContentSet(
                    "moveToEnd",
                    LAYOUT_CONTENT_NAMES.circuitTreeChart
                  );
                }}
              >
                <Icon type="bar-chart" />
              </Tag>
            </div>
            {nextLeafNerveDatas.map((dendrite) =>
              getNerveLeafData(dendrite.ind)
            )}
          </TreeNode>
        );
        return leafData;
      };
      const treeData = (this.options.pinnedSomaInds || []).map((pinnedSomaId) =>
        getNerveLeafData(pinnedSomaId)
      );
      return (
        <Layout
          class="barcharts-layout"
          style={{
            boxShadow: "rgb(1 1 1 / 30%) 0px 0px 10px",
          }}
        >
          <Layout.Header class="common-layout-header">
            <div
              class="layout-header-icon-box"
              onClick={() => {
                this.updateLayoutContentSet(
                  "delete",
                  LAYOUT_CONTENT_NAMES.circuitTreePanel
                );
              }}
            >
              <Icon
                type="close"
                class="layout-header-icon layout-header-icon-close"
              />
            </div>
            <Button
              size="small"
              onClick={async () => {
                await navigator.clipboard.writeText(
                  JSON.stringify(allNerveInds)
                );
                window.message.success("内容已复制");
              }}
            >
              复制所有ind
            </Button>
          </Layout.Header>
          <Layout.Content>
            <Card
              style={{
                width: "100%",
                height: "100%",
                overflow: "auto",
                // display: this.options.isShowPinnedSomaCircuitTreeMap ? "" : "none",
                overscrollBehavior: "contain",
              }}
              bodyStyle={{
                minWidth: "100.1%",
                minHeight: "100.1%",
                width: "fit-content",
              }}
            >
              <Tree
                blockNode={true}
                defaultExpandParent={true}
                defaultExpandAll={true}
                showLine={true}
              >
                {treeData}
              </Tree>
            </Card>
          </Layout.Content>
        </Layout>
      );
    },
    onCircuitTreeLeafContextmenu(e, data) {
      e.preventDefault();
      e.stopPropagation();
      this.updatepinnedNerveInds(data);
    },
    updatepinnedNerveInds(data) {
      const { getPartProp } = this;
      const item = data.ind;
      const newPinnedIds = new Set([...(this.options.pinnedNerveInds || [])]);
      newPinnedIds.has(item)
        ? newPinnedIds.delete(item)
        : newPinnedIds.add(item);
      this.updateOptions({
        pinnedNerveInds: [...newPinnedIds],
      });
    },
    renderSelector({
      options,
      onChange,
      style = {},
      mode = "multiple",
      value,
    } = {}) {
      return (
        <Select
          size="small"
          allowClear={true}
          mode={mode}
          onChange={onChange}
          style={{ width: "100%", ...style }}
          optionFilterProp="children"
          value={value}
        >
          {options
            .filter((p) => p)
            .map((p) => {
              p = [].concat(p);
              return <Select.Option key={p[0]}>{p[1] || p[0]}</Select.Option>;
            })}
        </Select>
      );
    },
    onClose() {
      this.showPanel(false);
    },
    toggleDrawer() {
      this.showPanel(!this.visible);
    },
    showRegion(regionName) {
      const hideRegions = new Set(this.options.hideRegions);
      hideRegions.delete(regionName);
      this.updateOptions({
        hideRegions: Array.from(hideRegions),
      });
    },
    hideRegion(regionName) {
      const hideRegions = new Set(this.options.hideRegions);
      hideRegions.add(regionName);
      this.updateOptions({
        hideRegions: Array.from(hideRegions),
      });
    },
  },
};
</script>

<style lang="less">
body {
  // 阻止抽屉组件对body样式的重写
  overflow: visible !important;
}

.panel-layout {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 10;
  background: transparent;
  pointer-events: none;
}

.slider-box {
  position: relative;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  background-color: white;
  padding: 0 10px 0 0;
  margin-left: -10px;
}

.ant-tooltip {
  pointer-events: none;
}

.show-part-nerve-box {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.pinned-list-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.glass-drawer {
  .ant-drawer-content-wrapper {
    width: "auto";
    background-color: rgba(0, 0, 0, 0.02);
  }

  .ant-drawer-content {
    opacity: 0;
    transition: 0.1s all;
  }

  &:hover {
    .ant-drawer-content {
      opacity: 1;
    }
  }
}

.timeline-search {
  width: 50px;

  &:focus {
    width: 200px;
  }
}

.nerve-tree-node {
  .ant-tree-node-content-wrapper {
    height: auto !important;
  }
}

.elevator-tab {
  .ant-tabs-content {
  }
}

.my-monaco-editor-layout {
  width: 100%;
  height: 100%;
}

.my-monaco-editor {
  width: 100%;
  height: 100%;
}

.barcharts-layout {
  background: white;
  width: 100%;
  height: 100%;
}

.barcharts-props-checkboxgroup {
  // margin-right: 50px;
  float: right;

  .ant-checkbox-wrapper {
    color: #fff;
  }
}

.common-layout-header {
  height: 32px;
  // height: fit-content;
  padding: 0 16px;
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
}

.layout-header-icon-box {
  // margin-left: 16px;
  // height: 40px;
  // width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  float: left;
  margin-right: 9px;
}

.layout-header-icon {
  border-radius: 100%;
  padding: 2px;
  color: rgba(1, 1, 1, 0.5);
  font-weight: bold;
  font-size: 9px;

  &-close {
    background: tomato;
  }

  &-save {
    background: #61c554;
  }
}

.panel-layout-content {
  > * {
    pointer-events: all;
  }
}

.chart-tooltip {
  pointer-events: none;
  padding: 10px;
  background-color: rgba(1, 1, 1, 0.6);
  border-radius: 10px;
  position: fixed;
  transform: translate(-50%, 0%);
  color: #fff;
  z-index: 500;
}

.bar-box {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: end;
  border-left: 1px dashed;
  border-bottom: 1px dashed;
  padding-top: 10px;
  padding-right: 2%;
}

.noBorderSelect {
  [role="combobox"] {
    border: 0;
  }
}

::-webkit-scrollbar {
  display: none;
}

.pixelDom {
  &:hover {
    border: 1px solid #61c554;
  }
}
</style>