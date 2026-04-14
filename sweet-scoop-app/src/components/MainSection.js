import React, {useState, useEffect} from "react";
import flavors from "../data/flavors";
import reviews from "../data/reviews";

function MainSection(){

const [randomFlavors,setRandomFlavors] = useState([]);
const [randomReviews,setRandomReviews] = useState([]);

useEffect(()=>{

const shuffledFlavors=[...flavors].sort(()=>0.5-Math.random());
setRandomFlavors(shuffledFlavors.slice(0,3));

const shuffledReviews=[...reviews].sort(()=>0.5-Math.random());
setRandomReviews(shuffledReviews.slice(0,2));

},[])

return(

<div className="main-section">

<h2>About Sweet Scoop</h2>
<p className="about-text">
Sweet Scoop offers a variety of delicious ice cream flavors made from fresh ingredients.
</p>

<h2>Featured Flavors</h2>

<div className="featured-flavors">

{randomFlavors.map(f=>(
<div className="flavor-card" key={f.id}>
<h4>{f.name}</h4>
<p>{f.price}</p>
</div>
))}

</div>

<h2>Customer Reviews</h2>

<div className="reviews">

{randomReviews.map((r,i)=>(
<div  key={i}>
<h4>{r.customerName}</h4>
<p>{r.review}</p>
<p>{"★".repeat(r.rating)}</p>
</div>
))}

</div>

</div>

)

}

export default MainSection;