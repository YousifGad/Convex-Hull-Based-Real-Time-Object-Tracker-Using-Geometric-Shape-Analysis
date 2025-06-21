import cv2

video = cv2.VideoCapture("rgb_ball_720.mp4")

# Get frame size and FPS from input video
width  = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = video.get(cv2.CAP_PROP_FPS)

# Define the video writer
out = cv2.VideoWriter("output_with_hull.avi", 
                      cv2.VideoWriter_fourcc(*'XVID'), 
                      fps, (width, height))

trail_points = []
area_list = []
vertex_list = []

while video.isOpened():
    flag, frame = video.read()
    if not flag:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    lower_red = (0, 130, 130)
    upper_red = (8, 255, 255)  

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.putText(frame, "Hull (Green)", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(frame, "Rect (Cyan)", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(frame, "Circle (Yellow)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        epsilon = 0.01 * cv2.arcLength(largest, True)
        smoothed = cv2.approxPolyDP(largest, epsilon, True)
        num_vertices = len(smoothed)
        vertex_list.append(num_vertices)
        hull = cv2.convexHull(smoothed)
        area = cv2.contourArea(hull)
        area_list.append(area)

        cv2.putText(frame, f"Area: {int(area)}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 1)
        cv2.putText(frame, f"Vertices: {num_vertices}", (10, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 255), 1)

        M = cv2.moments(largest)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
        
            trail_points.append((cx, cy))
            if len(trail_points) > 50:
                trail_points.pop(0)

        for i in range(1, len(trail_points)):
            cv2.line(frame, trail_points[i - 1], trail_points[i], (0, 0, 255), 2)

        cv2.drawContours(frame, [hull], -1, (0, 255, 0), 2)

        # Bounding rectangle
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)  # Cyan

        # Minimum enclosing circle
        (xc, yc), radius = cv2.minEnclosingCircle(largest)
        cv2.circle(frame, (int(xc), int(yc)), int(radius), (0, 255, 255), 2)  # Yellow


    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("Masked Ball", res)
    cv2.imshow("Tracked Ball with Convex Hull", frame)

    out.write(frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

with open("shape_data.csv", "w") as f:
    f.write("frame,area,num_vertices\n")
    for i in range(len(area_list)):
        f.write(f"{i},{area_list[i]},{vertex_list[i]}\n")


out.release()
video.release()
cv2.destroyAllWindows()