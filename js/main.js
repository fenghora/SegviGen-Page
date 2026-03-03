window.onload = function() {
    initWindow();
    // make_carousel('results-txt2', txt2_carousel_item_template, txt2_items, 2, 4);
    make_carousel('interactive_demo', interactive_demos_item_template, interactive_demos, 1, 1);
    make_carousel('full_segmentation', full_segmentation_item_template, full_segmentation_items, 2, 2);
    make_carousel('full_segmentation_2d', full_segmentation_w_2d_item_template, full_segmentation_2D_items, 2, 2);
    // make_carousel('results-img2', img2_carousel_item_template, img2_items, 2, 2);
    // make_carousel('results-txt2', txt2_carousel_item_template, txt2_items, 1, 2);
    // make_carousel('results-variants', variants_carousel_item_template, variants_items, 2, 1);
    // make_carousel('results-manipulation', manipulation_carousel_item_template, partaware_object_editing_manipulation_items, 1, 1);
    // make_carousel('results-manipulation-scene', manipulation_carousel_item_template, scene_editing_manipulation_items, 1, 1);
    // make_carousel('results-manipulation-gs', manipulation_carousel_item_template, gs_editing_manipulation_items, 1, 1);
    // make_selection_panel('results-scene', scene_selection_panel_thumbnail_template, scene_selection_panel_item_template, scene_items);
};
