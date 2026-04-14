import React from "react";
import flavors from "../data/flavors";
import FlavorItem from "./FlavorItem";

function FlavorCatalog({addToOrder}){

return(
<>

<h2>Ice Cream Flavors</h2>
    <div className="flavor-grid">

{flavors.map(f=>(
<FlavorItem
key={f.id}
flavor={f}
addToOrder={addToOrder}
/>
))}

</div>
</>
)

}

export default FlavorCatalog;