var interactive_demos = [
    {
        video: "assets/interactive_demo/1.mp4",
    },
    {
        video: "assets/interactive_demo/2.mp4",
    },
    {
        video: "assets/interactive_demo/3.mp4",
    },
    {
        video: "assets/interactive_demo/4.mp4",
    },
]


var full_segmentation_items =[
    // {
    //     video: "assets/full_segmentation/00aee5c2fef743d69421bb642d446a5b_combined.mp4",
    //     source_model: "assets/origanl_mesh/00aee5c2fef743d69421bb642d446a5b.glb",
    //     segmented_model: "assets/full_segmentation/00aee5c2fef743d69421bb642d446a5b.glb",
    // },
    {
        video: "assets/full_segmentation/01b8043112e74366a21256d5e64398fb_combined.mp4",
        source_model: "assets/origanl_mesh/01b8043112e74366a21256d5e64398fb.glb",
        segmented_model: "assets/full_segmentation/01b8043112e74366a21256d5e64398fb.glb",
    },
    {
        video: "assets/full_segmentation/0c070001a3904cd6809a31345475e930_combined.mp4",
        source_model: "assets/origanl_mesh/0c070001a3904cd6809a31345475e930.glb",
        segmented_model: "assets/full_segmentation/0c070001a3904cd6809a31345475e930.glb",
    },
    {
        video: "assets/full_segmentation/0c3ca2b32545416f8f1e6f0e87def1a6_combined.mp4",
        source_model: "assets/origanl_mesh/0c3ca2b32545416f8f1e6f0e87def1a6.glb",
        segmented_model: "assets/full_segmentation/0c3ca2b32545416f8f1e6f0e87def1a6.glb",
    },
    {
        video: "assets/full_segmentation/1b3e8b99913442308aa989e3f87680b3_combined.mp4",
        source_model: "assets/origanl_mesh/1b3e8b99913442308aa989e3f87680b3.glb",
        segmented_model: "assets/full_segmentation/1b3e8b99913442308aa989e3f87680b3.glb",
    },
    {
        video: "assets/full_segmentation/1c33b2e86c023a72905a5bea4ae713d0_combined.mp4",
        source_model: "assets/origanl_mesh/1c33b2e86c023a72905a5bea4ae713d0.glb",
        segmented_model: "assets/full_segmentation/1c33b2e86c023a72905a5bea4ae713d0.glb",
    },
    {
        video: "assets/full_segmentation/1ca8ea337fbc4bcfbeb3c633bc4c43f0_combined.mp4",
        source_model: "assets/origanl_mesh/1ca8ea337fbc4bcfbeb3c633bc4c43f0.glb",
        segmented_model: "assets/full_segmentation/1ca8ea337fbc4bcfbeb3c633bc4c43f0.glb",
    },
    {
        video: "assets/full_segmentation/2260799ee4e342398b64ab4ce8af1559_combined.mp4",
        source_model: "assets/origanl_mesh/2260799ee4e342398b64ab4ce8af1559.glb",
        segmented_model: "assets/full_segmentation/2260799ee4e342398b64ab4ce8af1559.glb",
    },
    {
        video: "assets/full_segmentation/226887c32c7a4a1f97de694e9bdbd10d_combined.mp4",
        source_model: "assets/origanl_mesh/226887c32c7a4a1f97de694e9bdbd10d.glb",
        segmented_model: "assets/full_segmentation/226887c32c7a4a1f97de694e9bdbd10d.glb",
    },
    {
        video: "assets/full_segmentation/2ae5cf2990c34e7db704f677de8de74c_combined.mp4",
        source_model: "assets/origanl_mesh/2ae5cf2990c34e7db704f677de8de74c.glb",
        segmented_model: "assets/full_segmentation/2ae5cf2990c34e7db704f677de8de74c.glb",
    },
    {
        video: "assets/full_segmentation/2ceb6778ac114101833e4c531544ada8_combined.mp4",
        source_model: "assets/origanl_mesh/2ceb6778ac114101833e4c531544ada8.glb",
        segmented_model: "assets/full_segmentation/2ceb6778ac114101833e4c531544ada8.glb",
    },
    {
        video: "assets/full_segmentation/3b204e1c8fa34183821cf925128f545c_combined.mp4",
        source_model: "assets/origanl_mesh/3b204e1c8fa34183821cf925128f545c.glb",
        segmented_model: "assets/full_segmentation/3b204e1c8fa34183821cf925128f545c.glb",
    },
    {
        video: "assets/full_segmentation/4b57e73e82ab400aa307adac36ea0e5e_combined.mp4",
        source_model: "assets/origanl_mesh/4b57e73e82ab400aa307adac36ea0e5e.glb",
        segmented_model: "assets/full_segmentation/4b57e73e82ab400aa307adac36ea0e5e.glb",
    },
]


function full_segmentation_item_template(item){
    return `<div class="x-card clickable" style="min-width: 240px" onclick=\'openWindow(base_window_template(${JSON.stringify(item)}))\'>
                <div class="x-labels">
                    <div class="x-label">GLB ✓</div>
                </div>
                <div style="width: 100%; aspect-ratio: 2 / 1;">
                    <video autoplay playsinline loop muted width="100%" src="${item.video}"
                    onerror="console.error('video error', this.src, this.error)"></video>
                </div>
            </div>`;
}


function base_window_template(item) {
    let prompt = `<div class="x-handwriting"></div>`;
    let panel = base_asset_panel_template(prompt);
    item = JSON.parse(JSON.stringify(item));
    return modelviewer_window_template(item, panel);
}



var full_segmentation_2D_items = [
    {
      prompt: "assets/outputs_2d/1/0c070001a3904cd6809a31345475e930.png",
      video: "assets/outputs_2d/1/0c070001a3904cd6809a31345475e930.mp4",
      source_model: "assets/origanl_mesh/0c070001a3904cd6809a31345475e930.glb",
      segmented_model: "assets/outputs_2d/1/0c070001a3904cd6809a31345475e930.glb",
    },
    {
      prompt: "assets/outputs_2d/10/3b204e1c8fa34183821cf925128f545c.png",
      video: "assets/outputs_2d/10/3b204e1c8fa34183821cf925128f545c.mp4",
      source_model: "assets/origanl_mesh/3b204e1c8fa34183821cf925128f545c.glb",
      segmented_model: "assets/outputs_2d/10/3b204e1c8fa34183821cf925128f545c.glb",
    },
    {
      prompt: "assets/outputs_2d/12/4b57e73e82ab400aa307adac36ea0e5e.png",
      video: "assets/outputs_2d/12/4b57e73e82ab400aa307adac36ea0e5e.mp4",
      source_model: "assets/origanl_mesh/4b57e73e82ab400aa307adac36ea0e5e.glb",
      segmented_model: "assets/outputs_2d/12/4b57e73e82ab400aa307adac36ea0e5e.glb",
    },
    {
      prompt: "assets/outputs_2d/13/226887c32c7a4a1f97de694e9bdbd10d.png",
      video: "assets/outputs_2d/13/226887c32c7a4a1f97de694e9bdbd10d.mp4",
      source_model: "assets/origanl_mesh/226887c32c7a4a1f97de694e9bdbd10d.glb",
      segmented_model: "assets/outputs_2d/13/226887c32c7a4a1f97de694e9bdbd10d.glb",
    },
    {
      prompt: "assets/outputs_2d/14/2260799ee4e342398b64ab4ce8af1559.png",
      video: "assets/outputs_2d/14/2260799ee4e342398b64ab4ce8af1559.mp4",
      source_model: "assets/origanl_mesh/2260799ee4e342398b64ab4ce8af1559.glb",
      segmented_model: "assets/outputs_2d/14/2260799ee4e342398b64ab4ce8af1559.glb",
    },
    {
      prompt: "assets/outputs_2d/2/1c33b2e86c023a72905a5bea4ae713d0.png",
      video: "assets/outputs_2d/2/1c33b2e86c023a72905a5bea4ae713d0.mp4",
      source_model: "assets/origanl_mesh/1c33b2e86c023a72905a5bea4ae713d0.glb",
      segmented_model: "assets/outputs_2d/2/1c33b2e86c023a72905a5bea4ae713d0.glb",
    },
    {
      prompt: "assets/outputs_2d/3/1ca8ea337fbc4bcfbeb3c633bc4c43f0.png",
      video: "assets/outputs_2d/3/1ca8ea337fbc4bcfbeb3c633bc4c43f0.mp4",
      source_model: "assets/origanl_mesh/1ca8ea337fbc4bcfbeb3c633bc4c43f0.glb",
      segmented_model: "assets/outputs_2d/3/1ca8ea337fbc4bcfbeb3c633bc4c43f0.glb",
    },
    {
      prompt: "assets/outputs_2d/4/2ae5cf2990c34e7db704f677de8de74c.png",
      video: "assets/outputs_2d/4/2ae5cf2990c34e7db704f677de8de74c.mp4",
      source_model: "assets/origanl_mesh/2ae5cf2990c34e7db704f677de8de74c.glb",
      segmented_model: "assets/outputs_2d/4/2ae5cf2990c34e7db704f677de8de74c.glb",
    },
    {
      prompt: "assets/outputs_2d/5/2ceb6778ac114101833e4c531544ada8.png",
      video: "assets/outputs_2d/5/2ceb6778ac114101833e4c531544ada8.mp4",
      source_model: "assets/origanl_mesh/2ceb6778ac114101833e4c531544ada8.glb",
      segmented_model: "assets/outputs_2d/5/2ceb6778ac114101833e4c531544ada8.glb",
    },
    {
      prompt: "assets/outputs_2d/6/00aee5c2fef743d69421bb642d446a5b.png",
      video: "assets/outputs_2d/6/00aee5c2fef743d69421bb642d446a5b.mp4",
      source_model: "assets/origanl_mesh/00aee5c2fef743d69421bb642d446a5b.glb",
      segmented_model: "assets/outputs_2d/6/00aee5c2fef743d69421bb642d446a5b.glb",
    },
    {
      prompt: "assets/outputs_2d/7/0c3ca2b32545416f8f1e6f0e87def1a6.png",
      video: "assets/outputs_2d/7/0c3ca2b32545416f8f1e6f0e87def1a6.mp4",
      source_model: "assets/origanl_mesh/0c3ca2b32545416f8f1e6f0e87def1a6.glb",
      segmented_model: "assets/outputs_2d/7/0c3ca2b32545416f8f1e6f0e87def1a6.glb",
    },
    {
      prompt: "assets/outputs_2d/8/01b8043112e74366a21256d5e64398fb.png",
      video: "assets/outputs_2d/8/01b8043112e74366a21256d5e64398fb.mp4",
      source_model: "assets/origanl_mesh/01b8043112e74366a21256d5e64398fb.glb",
      segmented_model: "assets/outputs_2d/8/01b8043112e74366a21256d5e64398fb.glb",
    },
    {
      prompt: "assets/outputs_2d/9/1b3e8b99913442308aa989e3f87680b3.png",
      video: "assets/outputs_2d/9/1b3e8b99913442308aa989e3f87680b3.mp4",
      source_model: "assets/origanl_mesh/1b3e8b99913442308aa989e3f87680b3.glb",
      segmented_model: "assets/outputs_2d/9/1b3e8b99913442308aa989e3f87680b3.glb",
    },
  ];


function full_segmentation_w_2d_item_template(item) {
    return `<div class="x-card clickable" style="min-width: 240px" onclick=\'openWindow(full_segmentation_w_2d_window_template(${JSON.stringify(item)}))\'>
                <div class="x-labels">
                    <div class="x-label">GLB ✓</div>
                </div>
                <div style="width: 100%; aspect-ratio: 2 / 1;">
                    <video autoplay playsinline loop muted width="100%" src="${item.video}"></video>
                </div>
                <div class="caption">
                    <div class="x-image-prompt_segmentation_w_2d">
                        <img src="${item.prompt}">
                    </div>
                </div>
            </div>`;
}


function full_segmentation_w_2d_window_template(item) {
    let prompt = `<div class="x-image-prompt"><img src="${item.prompt}"></div>`;
    let panel = asset_panel_template(prompt);
    item = JSON.parse(JSON.stringify(item));
    // item.model1 = item.model1
    return modelviewer_window_template(item, panel);
}


var interactive_segmentation_items = [
    {
        video: "assets/interactive_seg_results/032010.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_032010_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_032010_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/055759.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_055759_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_055759_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/060441.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_060441_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_060441_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/070343.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_070343_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_070343_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/070442.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_070442_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_070442_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/070535.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_070535_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_070535_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/070844.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_070844_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_070844_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/071018.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_071018_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_071018_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/071116.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_071116_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_071116_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/071303.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_071303_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_071303_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/071402.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_071402_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_071402_merge.glb",
    },
    {
        video: "assets/interactive_seg_results/071513.mp4",
        source_model: "assets/interactive_origin_mesh/segmented_mesh_20260228_071513_mesh.glb",
        segmented_model: "assets/interactive_seg_results/segmented_mesh_20260228_071513_merge.glb",
    }
];


function interactive_segmentation_item_template(item){
    return `<div class="x-card clickable" style="min-width: 240px" onclick=\'openWindow(base_window_template(${JSON.stringify(item)}))\'>
                <div class="x-labels">
                    <div class="x-label">GLB ✓</div>
                </div>
                <div style="width: 100%; aspect-ratio: 2 / 1;">
                    <video autoplay playsinline loop muted width="100%" src="${item.video}"
                    onerror="console.error('video error', this.src, this.error)"></video>
                </div>
            </div>`;
}


function txt2_carousel_item_template(item) {
    return `<div class="x-card clickable" style="min-width: 120px" onclick=\'openWindow(txt2_window_template(${JSON.stringify(item)}))\'>
                <div class="x-labels">
                    <div class="x-label">GLB ✓</div>
                </div>
                <div style="width: 100%; aspect-ratio: 2 / 1;">
                    <video autoplay playsinline loop muted width="100%" src="${item.video}"></video>
                    onerror="console.error('video error', this.src, this.error)">
                </div>
                <div class="caption">
                    <div class="x-handwriting">
                        ${item.prompt}
                    </div>
                </div>
            </div>`;
}


function interactive_demos_item_template(item) {
    return `<div id="teaser" style="display: flex; gap: 10px;">
                <video autoplay playsinline loop muted src="${item.video}" style="width: 100%;"></video>
            </div>`;
}


function img2_carousel_item_template(item) {
    return `<div class="x-card clickable" style="min-width: 240px" onclick=\'openWindow(img2_window_template(${JSON.stringify(item)}))\'>
                <div class="x-labels">
                    <div class="x-label">GLB ✓</div>
                </div>
                <div style="width: 100%; aspect-ratio: 2 / 1;">
                    <video autoplay playsinline loop muted width="100%" src="${item.video}"></video>
                </div>
                <div class="caption">
                    <div class="x-image-prompt">
                        <img src="${item.prompt}">
                    </div>
                </div>
            </div>`;
}


function txt2_window_template(item) {
    let prompt = `<div class="x-handwriting">${item.prompt}</div>`;
    let panel = asset_panel_template(prompt);
    item = JSON.parse(JSON.stringify(item));
    // item.model = 'assets/txt2/glbs/' + item.model
    return modelviewer_window_template(item, panel);
}


function img2_window_template(item) {
    let prompt = `<div class="x-image-prompt"><img src="${item.prompt}"></div>`;
    let panel = asset_panel_template(prompt);
    item = JSON.parse(JSON.stringify(item));
    // item.model1 = item.model1
    return modelviewer_window_template(item, panel);
}
