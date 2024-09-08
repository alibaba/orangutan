# Environment Configuration
## Step One: Python Environment
* Python Version: `3.9.x`
* Install Dependencies: `pip install numpy==1.22.3 pillow websocket-client simplejson`
## Step Two: Node.js Environment
* Node.js Version: `16.x`
* Install Dependencies:
  ```
  cd vue_server/
  npm install --force
  npm install jszip ws
  ```
## Step Three: Code Processing
Important!!! Due to the developer's negligence, there are some code remnants related to the personal working directory in the project, which may affect the normal operation of the project. To solve this problem, it is necessary to globally search `/Users/laola/CodeProject/Orangutan/` in the IDE and manually replace it with an empty string. The developer apologizes for any inconvenience caused and promises to fix this in subsequent updates.
# Run the Project
## Step One: Initialize the Neural Network
1. Modify the value of `CORTEX_OPTS` in the file `consts/experiment.py`:
   ```
   CORTEX_OPTS = [
       init_mock_input_and_percept_feature,
       run_mock_input_and_percept_feature,
   ][0]
   ```
2. Run in the console: `$ python cortex.py`, wait for initialization to finish
3. The structural data of the neural network will be saved in the path `experiments/mnist/datas/save/save_init`, occupying an estimated space of 11.66 GB.
## Step Two: Run the Neural Network
1. Modify the value of `CORTEX_OPTS` in the file `consts/experiment.py`:
   ```
   CORTEX_OPTS = [
       init_mock_input_and_percept_feature,
       run_mock_input_and_percept_feature,
   ][1]
   ```
2. Run in the console: `$ python cortex.py`, wait for the neural network to finish running
3. The running records of the neural network will be saved in the path `experiments/mnist/datas/history`, with each number occupying around 1.2GB of space.
4. The model can be configured to observe multiple digits at once by modifying the `RUN_CORTEX_OPTS` object in the file `consts/experiment_config/mock_input_and_percept_feature.py`, for example:
   ```
   RUN_CORTEX _OPTS={
       ...
       # Observe digits 0 to 9, observing 10 images for each digit
       "MNIST_INPUTS_LIST": [f'{i}_{j}' for i in range(10) for j in range(10)][::-1],
       ...
   }
   ```
## Step Three: View the Network's Running Results
1. Start the Python service, run in the console:
   ```
   python web_socket.py
   ```
2. Start the Node.js service, run in the console:
   ```
   cd vue_server/node_server
   node index.js
   ```
3. Start the frontend service, run in the console:
   ```
   cd vue_server
   npm run serve
   ```
4. Access the address `http://localhost:8081/` in a browser, where you can see the initial interface:
   ![image](https://github.com/user-attachments/assets/a6417576-c6e3-4043-a3e4-d9e68ac3aebb)
6. Press `Command+Option+J` (or `Ctrl+Shift+J` on windows) to open the console, copy the following content, paste it into the console, and press enter:
   ```
   localStorage.setItem('OptionStore',`{"panelShow":true,"showSomaProps":[],"showNerveProps":[],"showPinnedSomaNerveType":"out","isShowPinnedSomaCircuit":false,"hideRestingNerve":false,"onlyShowHistoryFileNames":["attention_result"],"elevatorAnchor":{},"highlightStaticPart":{},"regionOffsetX":{},"regionHighlightNeuronRegExp":{},"nowaFormProcess":"","hideRegions":[],"layoutSize":"normal","readFileName":"8_3;attention_result;4_0","searchNerveExpressions":[{"content":"# dot_matrix\\nreturns['search_nerve_inds'] = get_soma_inds('point', 'input')\\nreturns['search_nerve_prop_names'] = [\\n    'excite',\\n]\\nreturns['search_nerve_result_limit'] = 2000","isCompressed":true,"chartShowProps":[]},{"content":"# attention_competition_result\\nangle_inds = np.array([\\n    get_soma_inds(\\n        f'angle', \\n        f'attention_competition_result_of_angle_of_orientation{orient}_and_{(orient+angle)%360 or 360.0}',\\n    ).reshape((28,28)) \\n    for orient in ORIENTS \\n    for angle in ANGLES \\n])\\ncontour_center_inds =np.array([get_soma_inds(\\n        f'contour_center',\\n        f'attention_competition_result_of_inner_contour_center'\\n    ).reshape((28,28))])\\nall_feature_inds = np.concatenate((angle_inds, contour_center_inds))\\nargmax_ind=np.argmax(cortex['excite'][all_feature_inds], axis=0)\\nmax_all_feature_inds=all_feature_inds[argmax_ind.flatten(),np.repeat(np.arange(28),28),np.tile(np.arange(28),28)]\\n\\nreturns['search_nerve_inds'] = max_all_feature_inds\\nreturns['search_nerve_prop_names'] = [\\n    'excite',\\n]\\nreturns['search_nerve_result_limit'] = 2000","isCompressed":true,"chartSetting":{"showType":"image","contentInfos":[{"name":"# attention_competition_result","zoom":"0.3","G":"0","B":"0","highlightPixelIndex":0},{"name":"# dot_matrix"}],"contentInfoOffsets":[null,"-1"]}},{"content":"# Neural Attributes(Properties)\\ninds = np.concatenate(\\n    tuple([\\n        get_soma_inds(f'attribute-{prop_type}', f'{prop_name}_single_coding') \\n        for abstract_type_ind, (prop_type, prop_values) in enumerate(\\n            COMMON_ABSTRACT_NAMES_WITH_ABSTRACT_TYPES.items()) \\n        for prop_name, _ in prop_values\\n    ])\\n)\\n\\nreturns['search_nerve_inds'] = inds\\nreturns['search_nerve_prop_names'] = [\\n    'excite',\\n]\\nreturns['search_nerve_result_limit'] = 2000","isCompressed":true,"chartShowProp":"excite","chartSetting":{"showType":"bar","contentInfos":[{"name":"# Neural Attributes(Properties)"}],"radioOrCheckbox":"radio"}}],"layoutContentSet":["cortex","searchNerveChart"],"searchNerveChartInd":1,"searchNerveEditorInd":1,"showSider":true,"leftDrawerTabsActiveKey":"2"}`)
   ```
   ![image](https://github.com/user-attachments/assets/872d30d8-ce5b-4dfd-8e5d-0323867248c7)
7. Refresh the page to see the following interface. The main parts include: 1. Search for a specified group of neurons, 2. View search results button, 3. Search results, 4. Filter for key nodes in the timeline, 5. Timeline to drag and view the neural network's state at different time nodes:
   ![image](https://github.com/user-attachments/assets/4440c688-5203-47d8-ab4f-82ddf7d10a96)
8. By default, it displays the changing process of attention competition results. To view the abstract properties of each featured observed, set the right-hand side `time node filter` option to `percept_properties` and click the third filter condition's view button, as shown in the image:
   ![image](https://github.com/user-attachments/assets/f66870ff-a4fa-445b-88a2-152509611c15)
