
export function dashboard(view) {
    const regions = new Map(Array.from(view.querySelectorAll('[data-region]'), n => [n.dataset.region, {
      node: n,
    }]));
    view.oninput = view.onchange = view.onclick = e => e.stopImmediatePropagation();
    view.value = function(region, content, invalidate) {
      const {node} = regions.get(region);
      node.appendChild(content);
      
      const remove = () => { if(content.parentNode === node) node.removeChild(content) };
      if(invalidate) invalidate.then(remove);
      return remove;
    };
    return view;
  }