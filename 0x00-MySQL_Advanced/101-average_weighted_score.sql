-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Create the procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update the average_score for each user based on weighted scores
    UPDATE users u
    JOIN (
        SELECT 
            c.user_id,
            SUM(c.score * p.weight) / SUM(p.weight) AS weighted_avg
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        GROUP BY c.user_id
    ) sub ON u.id = sub.user_id
    SET u.average_score = sub.weighted_avg;
END //

-- Reset the delimiter
DELIMITER ;
