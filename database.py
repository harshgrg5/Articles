from typing import List, Optional
from models import Article, ArticleCreate
from datetime import datetime

# Real sample article dataset provided by user
SAMPLE_ARTICLES: List[dict] = [
    {
        "id": 4,
        "title": "Home office as a driver for VR Applications",
        "created_at": "2025-03-27T03:55:47.044655Z",
        "prompt": "Virtual Realms",
        "short_description": "Remote work has become the norm post-pandemic, offering employees flexibility and productivity benefits. - Working from home allows for flexible hours and location independence, contributing to increased business productivity. - Virtual offices aim to recreate the office environment in a remote setting, enhancing comfort and productivity for remote workers.",
        "content": "- Virtual reality (VR) creates computer-generated immersive environments, allowing users to engage with 3D worlds and interact with virtual objects. - VR technology has the potential to transform various aspects of life, including work, by providing realistic virtual environments for interaction and collaboration.\r\n\r\n\r\n- Create Professional Image: Virtual offices provide a professional business address, enhancing credibility and trustworthiness for businesses. - More Flexible Expansion Opportunities: Virtual offices allow for expansion into new markets without the need for physical relocation, reducing costs and increasing flexibility. - Cost Saving: Virtual offices offer cost-saving benefits compared to traditional office spaces, providing reputable business addresses at a lower cost. - Better Productivity: Virtual offices minimize office interruptions, leading to improved productivity in a peaceful environment. - Optional Business Support Services: Virtual office packages often include services such as call answering and mail handling, freeing up time for core business activities. - More Independence: Remote work in virtual offices allows for more independence in task management and prioritization, enabling employees to focus on their responsibilities.\r\n\r\n\r\n- Virtual reality extends beyond gaming to create immersive work environments for remote teams. - VR technology facilitates natural collaboration and communication in virtual office settings, overcoming challenges of remote work. - Virtual reality applications enable real-time collaboration and idea exchange among coworkers, enhancing productivity and connectivity in remote work setups.",
        "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-04-19_10-40-08_5991.webp"
    },
    {
        "id": 3,
        "title": "The Future of Virtual Reality: Prepare to Be Amazed in 2023!",
        "created_at": "2025-03-27T03:55:30.815007Z",
        "prompt": "Articles",
        "short_description": "VR has evolved beyond gaming and entertainment, impacting various sectors like healthcare, education, and training. It's transforming how we connect and design, offering unprecedented experiences.",
        "content": "VR gaming has reached new levels of sophistication, while its role in professional training and product visualization is expanding. VR provides realistic training environments and enhances customer engagement.\r\n\r\n\r\nVR gaming has reached new levels of sophistication, while its role in professional training and product visualization is expanding. VR provides realistic training environments and enhances customer engagement.\r\n\r\n\r\nAnticipation for new headset releases grows in 2023, with a focus on more powerful and sleek designs. Hand tracking gains traction for intuitive VR interactions, potentially becoming the standard. The future promises continued hardware advancements and immersive experiences.\r\n\r\n\r\nVR pushes boundaries by engaging all senses, not just visual. Hyper-realistic simulations offer opportunities in entertainment, education, and therapy. The technology blurs the line between virtual and real, promising endless possibilities for impactful experiences.",
        "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-03-29_18-59-35_9996.webp"
    },
    {
        "id": 2,
        "title": "From Virtual Dreams to Reality: The Ultimate Guide to Metaverse Trends in 2024!",
        "created_at": "2025-03-27T03:55:13.343812Z",
        "prompt": "Virtual Realms",
        "short_description": "The digital landscape is undergoing a transformative revolution, propelled by the escalating integration of 3D technologies spanning various industries. This seismic shift is seamlessly weaving together virtual and augmented reality, artificial intelligence, and blockchain, creating an immersive and interconnected digital space.",
        "content": "The digital landscape is undergoing a transformative revolution, propelled by the escalating integration of 3D technologies spanning various industries. This seismic shift is seamlessly weaving together virtual and augmented reality, artificial intelligence, and blockchain, creating an immersive and interconnected digital space. As the metaverse edges closer to realization in 2024, it heralds a paradigm shift in our interaction with the digital realm. This blog delves deep into the forefront of this evolution, exploring the major metaverse trends poised to reshape the upcoming year. Brace yourself for a journey into the dynamic convergence of cutting-edge technologies that are set to redefine the way we perceive, engage, and navigate the vast expanse of the metaverse in the coming months. The metaverse is not just a concept; it's an imminent reality that promises to reshape the digital landscape as we know it.\r\n\r\n\r\nThe metaverse has transcended its initial identity as merely a gaming or entertainment realm, evolving into a distinct and vibrant digital economy. Through the use of virtual currencies, participants in this virtual space have created a complex ecosystem where they trade, buy, and sell virtual goods and services. Users are empowered to generate income by creating, monetizing, and exchanging an array of digital assets, spanning from virtual real estate and in-game items to digital art. This digital economy, though mirroring real-world market dynamics, operates uniquely within the boundaries of virtual worlds, often leveraging blockchain technology to ensure secure and equitable transactions.",
        "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-03-29_18-57-38_1198.webp"
    },
    {
        "id": 1,
        "title": "Is virtual reality a future?",
        "created_at": "2025-03-27T03:54:48.746262Z",
        "prompt": "Virtual Realms",
        "short_description": "Virtual reality has been with us for a long time and quite a few of us have had a chance to touch, feel and experience it firsthand. I myself have had privilege of owning 4-5 headsets from Google cardboard box to Meta Oculus 2 /3 to now proudly owning Apple Vision Pro.",
        "content": "Virtual reality has been with us for a long time and quite a few of us have had a chance to touch, feel and experience it firsthand. I myself have had privilege of owning 4-5 headsets from Google cardboard box to Meta Oculus 2 /3 to now proudly owning Apple Vision Pro. I have extensively used them, if I was to sum up, I would say close 400 hours of Movies, playing tennis or boxing and watching YouTube. So yes, I have had a great deal of experience.\r\n\r\n\r\nYou can’t compare virtual reality headset to your phones or to your computers. They are in their league of their own.",
        "image_url": "https://storage.googleapis.com/stylefixtailoringnextjsassets/testimages/2024-03-29_16-54-04_3302.webp"
    }
]


class ArticleRepository:
    def __init__(self):
        self._articles = [Article(**item) for item in SAMPLE_ARTICLES]
        self._next_id = max(a.id for a in self._articles) + 1 if self._articles else 1

    def get_all(
        self,
        prompt: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> tuple[List[Article], int]:
        filtered = self._articles

        if prompt:
            prompt_lower = prompt.strip().lower()
            filtered = [a for a in filtered if a.prompt and a.prompt.lower() == prompt_lower]

        if search:
            search_lower = search.strip().lower()
            filtered = [
                a for a in filtered
                if search_lower in a.title.lower()
                or search_lower in a.short_description.lower()
                or search_lower in a.content.lower()
            ]

        total_count = len(filtered)
        paginated = filtered[offset : offset + limit]
        return paginated, total_count

    def get_by_id(self, article_id: int) -> Optional[Article]:
        for article in self._articles:
            if article.id == article_id:
                return article
        return None

    def create(self, article_in: ArticleCreate) -> Article:
        now_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        article = Article(
            id=self._next_id,
            created_at=now_str,
            **article_in.model_dump()
        )
        self._articles.append(article)
        self._next_id += 1
        return article


# Global repository instance
db_repo = ArticleRepository()
