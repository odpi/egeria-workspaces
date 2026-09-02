There are two types of feedback that we want to support:
1) When we are running the demo version with external users, we want to be able to capture their feedback on the experience, the content, and the capabilities. This will help us to understand how users are engaging with the system, what they find useful, and where there are opportunities for improvement. 
I'd like a feedback button on every page/view so that we can easily capture user feedback in the moment. This could be a simple form that allows users to rate their experience and provide comments or suggestions. We can also include an option for users to provide their contact information if they are open to being contacted for follow-up discussions.
We should track this feedback, along with the time, external user id, and the page/view they were on when they submitted the feedback. This will allow us to analyze the feedback in the context of the user experience and to identify patterns or trends in the feedback we receive.
2) Egeria and pyegeria has an internal feedback API that supports:
Likes, Ratings and Comments on any Egeria object. We need to start to think about how we support this in Egeria-Explorer in particular.
This will probably be an iterative process. 
3) A good place to start might be Likes and Ratings. Users may want to filter on likes and ratings - especially in Products, Glossary and Reports but perhaps more broadly.
4) Comments are more complex - but they are also more powerful. They allow users to provide more detailed feedback and to engage in discussions about specific Egeria objects. We will need to think about how to support comments in a way that is user-friendly and that encourages constructive feedback and discussion.

What are some of the design approaches and best practices to consider?

Review the Egeria feedback API documentation to understand the capabilities and limitations of the API, and to identify any specific requirements or constraints that we need to consider in our design.



