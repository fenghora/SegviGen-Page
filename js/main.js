window.onload = function() {
    initWindow();
    make_carousel('interactive_demo', interactive_demos_item_template, interactive_demos, 1, 1);
    make_carousel('interactive_segmentation', interactive_segmentation_item_template, interactive_segmentation_items, 2, 2);
    make_carousel('full_segmentation', full_segmentation_item_template, full_segmentation_items, 2, 2);
    make_carousel('full_segmentation_2d', full_segmentation_w_2d_item_template, full_segmentation_2D_items, 2, 2);
};
